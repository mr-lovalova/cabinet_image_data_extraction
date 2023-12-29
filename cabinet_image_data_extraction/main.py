import os
import sys

sys.path.append(".")
from pathlib import Path
from PIL import Image
import torch
import click

from box import Box
import extract
import item
import serializers

from config import MODEL_PATH, RESULTS_FILE_PATH, DESTINATION_PATH


def get_img(root, file):
    if file.lower().endswith("jpg"):
        img = Image.open(Path(f"{root}/{file}"))
    else:
        img = None
    return img


def get_detection_model(conf):
    model = torch.hub.load("ultralytics/yolov5", "custom", MODEL_PATH)
    model.conf = conf
    return model


def get_tree(path):
    tree = os.walk(path, topdown=True)
    next(tree)  # skipping top directory
    return tree


def ensure_destination_folder(destination):
    destination.mkdir(exist_ok=True)


def start_empty_results_file(file_path):
    with open(file_path, "w"):
        pass


@click.command()
@click.option("--source", default="data/raw", help="Path to image folders")
@click.option("--output_format", default="JSON")
@click.option("--conf", default=0.8, help="confidence of detection model")
def main(source, output_format, conf):
    source = Path(source)
    destination = Path(DESTINATION_PATH)
    results_file = Path(RESULTS_FILE_PATH)

    ensure_destination_folder(destination)
    start_empty_results_file(results_file)

    model = get_detection_model(conf)
    tree = get_tree(source)
    logger = item.Logger(destination)

    for root, _, files in tree:
        id_ = root.split("/")[-1]
        box = Box(id_)
        logger.start(id_)
        for file in files:
            img = get_img(root, file)
            if not img:
                continue
            extractions = extract.from_img(model, img, logger=logger)
            for extraction in extractions:
                if extraction.is_valid:
                    box.add(extraction)
                logger.log(extraction)

        with open(results_file, "a") as f:
            f.write(serializers.serializer.serialize(box, output_format) + "\n")

    logger.recap()


if __name__ == "__main__":
    main()

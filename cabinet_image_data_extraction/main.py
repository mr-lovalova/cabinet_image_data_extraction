import os
import sys
import re

from pathlib import Path
from PIL import Image
import torch
import click
from ultralytics import YOLO

sys.path.append(".")
from box import Box
import extract
import item
import serializers
import matplotlib.pyplot as plt
from config import MODEL_PATH, RESULTS_FILE_PATH, DESTINATION_PATH


def get_img(root, file):
    if file.lower().endswith("jpg"):
        img = Image.open(Path(f"{root}/{file}"))
    else:
        img = None
    return img


def get_detection_model(conf):
    # model = torch.hub.load("ultralytics/yolov5", "custom", MODEL_PATH)  # yolov5
    model = YOLO(MODEL_PATH, task="detect")
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


def parse_id(folder):
    try:
        station_id, cabinet_number = re.findall(r"\d+", folder)
    except ValueError:  # folder has the wrong format
        return None
    cabinet_number = int(cabinet_number.lstrip("0"))
    station_id = int(station_id.lstrip("0"))
    return f"{station_id}-{cabinet_number}"


@click.command()
@click.option("--source", default="data/raw3", help="Path to facility archive")
@click.option("--output_format", default="JSON")
@click.option("--conf", default=0.7, help="confidence of detection model")
@click.option("--development_mode", is_flag=True, default=True)
def main(source, output_format, conf, development_mode):
    source = Path(source)
    destination = Path(DESTINATION_PATH)
    results_file = Path(RESULTS_FILE_PATH)

    ensure_destination_folder(destination)
    start_empty_results_file(results_file)

    model = get_detection_model(conf)
    tree = get_tree(source)
    logger = item.Logger(destination, development_mode)

    for root, _, files in tree:
        id_ = parse_id(root.split("/")[-1])
        if not id_:
            continue
        box = Box(id_)
        logger.start(id_)
        for file in files:
            img = get_img(root, file)
            if not img:
                continue
            extractions = extract.from_img(model, img, box=box)
            print(f"FOUND {len(extractions)} LABELS ON IMAGE {file}")
            for extraction in extractions:
                if extraction.is_valid:
                    box.add_object(extraction)

                logger.log(extraction)

        with open(results_file, "a") as f:
            f.write(serializers.serializer.serialize(box, output_format) + "\n")

    logger.recap()


if __name__ == "__main__":
    main()

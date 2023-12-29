import os
import json
from pathlib import Path
from PIL import Image
import torch
import click

from box import Box
import extract
import item
import serializers


def get_img(root, file):
    if file.lower().endswith("jpg"):
        img = Image.open(Path(f"{root}/{file}"))
    else:
        img = None
    return img


def setup(path, conf, dest):
    path = Path(path)
    model = torch.hub.load("ultralytics/yolov5", "custom", "models/model.onnx")
    model.conf = conf
    Path(dest).mkdir(exist_ok=True)
    return path, model


def start_file(path):
    with open(path, "w"):
        pass


def get_tree(path):
    tree = os.walk(path, topdown=True)
    next(tree)  # skipping top directory
    return tree


@click.command()
@click.option(
    "--path",
    default="data/raw",
    help="Folder containing subfolders with images",
)
@click.option("--conf", default=0.8, help="Confidence of object detection model")
def main(path, conf, dest="results2/"):  # rename dir to path
    path, model = setup(path, conf, dest)
    results_file = dest + "results.txt"
    start_file(results_file)
    tree = get_tree(path)
    logger = item.Logger(dest)
    serializer = serializers.ObjectSerializer()

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
            print("VARS", dict(vars(box)))
            print("type:", type(vars(box)))
            print("SERIALIZED", serializer.serialize(box, "JSON"))
            # f.write(str(vars(box)) + "\n")
            f.write(serializer.serialize(box, "JSON") + "\n")

    # print(logger.resume())


if __name__ == "__main__":
    main()

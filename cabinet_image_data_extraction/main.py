import os
import json
from pathlib import Path
from PIL import Image
import torch
import click

from box import Box
import extract
from logger import Logger


def get_img(root, file):
    if file.lower().endswith("jpg"):
        img = Image.open(Path(f"{root}/{file}"))
    else:
        img = None
    return img


def as_json(boxes):
    out = {}
    for box in boxes:
        out[box.id] = box.asdict()
    return json.dumps(out, indent=4, ensure_ascii=False)


def save(file, folder, format_="JSON"):
    destination = folder + "results.json"
    if format_ == "JSON":
        with open(destination, "w", encoding="utf-8") as outfile:
            outfile.write(file)
    else:
        raise NotImplementedError("Format not implemented")


def setup(path, conf, dest):
    path = Path(path)
    model = torch.hub.load("ultralytics/yolov5", "custom", "models/model.onnx")
    model.conf = conf
    Path(dest).mkdir(exist_ok=True)
    return path, model


def start_file(path):
    with open(path, "w"):
        pass


@click.command()
@click.option(
    "--path",
    default="data/raw",
    help="Folder containing subfolders with images",
)
@click.option("--verbose", "-v", is_flag=True, help="Will print verbose messages.")
@click.option("--conf", default=0.8, help="Confidence of object detection model")
@click.option("--num_images", default=-1, help="Number of images to do detection from")
def main(path, num_images, conf, verbose, dest="results2/"):  # rename dir to path
    path, model = setup(path, conf, dest)
    results_file = dest + "results.txt"
    start_file(results_file)
    tree = os.walk(path, topdown=False)
    logger = Logger(dest)

    for root, _, files in tree:
        id_ = root.split("/")[-1]
        box = Box(id_)
        logger.start(id_)
        for file in files:
            img = get_img(root, file)
            if not img:
                continue
            extractions = extract.from_img(model, img, logger=logger)
            for item in extractions:
                if item.is_valid:
                    box.add(item)
                logger.log(item)

        with open(results_file, "a") as f:
            f.write(str(vars(box)) + "\n")


if __name__ == "__main__":
    main()

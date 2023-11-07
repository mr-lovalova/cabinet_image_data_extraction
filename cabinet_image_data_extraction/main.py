import os
import json
from pathlib import Path
import torch
import click
from PIL import Image
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


def save(json_, folder):
    destination = folder + "results.json"
    with open(destination, "w", encoding="utf-8") as outfile:
        outfile.write(json_)


def setup(path, conf, dest):
    path = Path(path)
    model = torch.hub.load("ultralytics/yolov5", "custom", "models/model.onnx")
    model.conf = conf
    Path(dest).mkdir(exist_ok=True)
    return path, model


@click.command()
@click.option(
    "--path",
    default="/Users/andersskottlind/Desktop/billeder",
    help="Folder containing subfolders with images",
)
@click.option("--verbose", "-v", is_flag=True, help="Will print verbose messages.")
@click.option("--conf", default=0.8, help="Confidence of object detection model")
@click.option("--num_images", default=-1, help="Number of images to do detection from")
def main(path, num_images, conf, verbose, dest="results2/"):  # rename dir path
    path, model = setup(path, conf, dest)
    boxes = set()
    tree = os.walk(path, topdown=False)

    for root, _, files in tree:
        id_ = root.split("/")[-1]
        box = Box(id_)
        boxes.add(box)
        logger = Logger(dest, id_) # Maybe tchange loggre to do all saving insetad of usingset of pxoes
        for file in files:
            img = get_img(root, file)
            if not img:
                continue
            extractions = extract.from_img(model, img, logger=logger)
            for item in extractions:
                box.add(item)
            logger.save()
            logger.log()

    # json_ = as_json(boxes)
    # save(json_, dest)


if __name__ == "__main__":
    main()

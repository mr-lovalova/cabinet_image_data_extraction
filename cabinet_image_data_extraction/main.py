import os
import json
from pathlib import Path
import torch
import click
from PIL import Image
from box import Box
import objects


def get_img(root, file):
    if file.lower().endswith("jpg"):
        img = Image.open(Path(f"{root}/{file}"))
    else:
        img = None
    return img


def extract_from_img(model, img):
    detections = model(img).crop(save=False)
    extractions = []
    for crop in detections:
        extracted = extract_from_detection(crop)
        if extracted:
            extractions.append(extracted)
    return extractions


def extract_from_detection(crop):
    prediction, _ = crop["label"].split()  # old/yellow/black
    if prediction != "black":  # temp until new model without y/b
        return None
    return objects.factory.create(prediction, image=crop["im"])


def as_json(boxes):
    out = {}
    for box in boxes:
        out[box.id] = box.asdict()
    return json.dumps(out, indent=4, ensure_ascii=False)


def save(json_, destination="results2.json"):
    with open(destination, "w", encoding="utf-8") as outfile:
        outfile.write(json_)


@click.command()
@click.option(
    "--path",
    default="/Users/andersskottlind/Desktop/billeder",
    help="Folder containing subfolders with images",
)
@click.option("--verbose", "-v", is_flag=True, help="Will print verbose messages.")
@click.option("--conf", default=0.8, help="Confidence of object detection model")
@click.option("--num_images", default=-1, help="Number of images to do detection from")
def main(path, num_images, conf, verbose):  # rename dir path
    path = Path(path)
    model = torch.hub.load("ultralytics/yolov5", "custom", "models/model.onnx")
    model.conf = conf
    boxes = set()

    tree = os.walk(path, topdown=False)
    for root, _, files in tree:
        box = Box(id_=root.split("/")[-1])
        boxes.add(box)
        for file in files:
            img = get_img(root, file)
            if not img:
                continue
            extractions = extract_from_img(model, img)
            for item in extractions:
                box.add(item)
            print("BOX LABELS", box.asdict())

    json_ = as_json(boxes)
    save(json_)


if __name__ == "__main__":
    main()

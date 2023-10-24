import os
import json
from pathlib import Path
import torch
import click
from PIL import Image
from box import Box
import extract


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


def log_item(item, folder, box_id, count):
    destination = folder + box_id + "/"
    Path(destination).mkdir(exist_ok=True)
    Image.fromarray(item.clean_img).save(destination + f"{str(count)}clean.jpg")
    Image.fromarray(item.img).save(destination + f"{str(count)}original.jpg")
    item.clean_img = None
    item.img = None
    with open(destination + f"{str(count)}.txt", "w", encoding="utf-8") as f:
        f.write(item.text)


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
        for file in files:
            img = get_img(root, file)
            if not img:
                continue
            extractions = extract.from_img(model, img)
            for count, item in enumerate(extractions):
                log_item(item, dest, id_, count)
                box.add(item)
            print("BOX LABELS", box.asdict())

    json_ = as_json(boxes)
    save(json_, dest)


if __name__ == "__main__":
    main()

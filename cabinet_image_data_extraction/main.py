import json
import torch
import click
import os
from pathlib import Path
from PIL import Image
from box import Box
import items


@click.command()
@click.option(
    "--path",
    default="/Users/andersskottlind/Desktop/billeder",
    help="Folder containing subfolders with images",
)
@click.option("--verbose", "-v", is_flag=True, help="Will print verbose messages.")
@click.option("--conf", default=0.8, help="Confidence of object detection model")
@click.option("--num_images", default=-1, help="Number of images to do detection from")
@click.option(
    "--save",
    "-s",
    is_flag=True,
    help="Will save example crops with their predicted text.",
)
def cli(path, num_images, conf, verbose, save):  # rename dir path
    path = Path(path)
    model = torch.hub.load("ultralytics/yolov5", "custom", "models/model.onnx")
    model.conf = conf
    boxes = set()

    tree = os.walk(path, topdown=False)
    for root, _, files in tree:
        for file in files:
            if file.lower().endswith("jpg"):
                location = Path(f"{root}/{file}")
                img = Image.open(location)
                if not img:
                    continue
                box_id = root.split("/")[-1]
                box = Box(box_id)
                boxes.add(box)
                result = model(img)
                cropped = result.crop(save=False)
                if verbose:
                    click.echo(f"Doing inference on image at: {location}")
                    click.echo(f"Detected {len(cropped)} labels")
                for count, crop in enumerate(cropped):
                    prediction, _ = crop["label"].split()  # old/yellow/black
                    if prediction != "black":  # temp until new model without y/b
                        continue
                    object_ = items.factory.create(prediction, image=crop["im"])
                    if object_ is None:
                        continue
                    box.add(object_, prediction)
                print("BOX LABELS", box.items)

    # save_results(boxes)

    return boxes


def save_results(boxes):
    out = {}
    total_labels = 0
    added_labels = 0
    for box in boxes:
        out[box.id] = box.asdict()
        if box.num_labels:
            added_labels += 1
            total_labels += box.num_labels
    json_object = json.dumps(out, indent=4, ensure_ascii=False)
    print(json_object)
    # with open("results.json", "w") as outfile:
    #    outfile.write(json_object)

    click.echo("________________________________________________________")
    click.echo(
        f"Added labels to {added_labels} boxes out of {len(boxes)} ({round(added_labels/len(boxes)* 100,0)}%)"
    )
    click.echo(f"with an average of {round(total_labels/len(boxes),2)} per box")
    click.echo(
        f"and an average of {round(total_labels/added_labels,2)} per box labeled box"
    )


if __name__ == "__main__":
    boxes = cli()
    save_results(boxes)

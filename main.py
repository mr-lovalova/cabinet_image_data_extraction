import json
import torch
import click
import os
from pathlib import Path
from PIL import Image

from get_images import image_walk
from box import Box
from get_text import extract_text, process_label


@click.command()
@click.option(
    "--dir",
    default="/Users/andersskottlind/Desktop/billeder",
    help="Folder containing subfolders with images",
)
@click.option("--verbose", "-v", is_flag=True, help="Will print verbose messages.")
@click.option("--conf", default=0.75, help="Confidence of object detection model")
@click.option("--num_images", default=50, help="Number of images to do detection from")
@click.option(
    "--save",
    "-s",
    is_flag=True,
    help="Will save example crops with their predicted text.",
)
def cli(dir, num_images, conf, verbose, save):
    dir = Path(dir)
    model = torch.hub.load("ultralytics/yolov5", "custom", "best.onnx")
    model.conf = conf
    images = image_walk(dir, num_images)
    boxes = set()
    for image in images:
        if save:
            path = Path(f"results/{image.box}/")
            try:
                os.makedirs(path)
            except OSError:
                pass
        image_box = Box(image.box)
        if image_box not in boxes:
            box = image_box
            boxes.add(box)
        result = model(image.img)
        cropped = result.crop(save=False)
        if verbose:
            click.echo(f"Doing inference on image at: {image.location}")
            click.echo(f"Detected {len(cropped)} labels")
        for count, crop in enumerate(cropped):
            label_type, _ = crop["label"].split()
            clean_img, rot = process_label(crop["im"], label_type)
            if clean_img is None:
                continue
            label_text = extract_text(clean_img)
            if verbose:
                click.echo(f"Extracted text from Label {count}: {label_text}")
            box.add_label(label_text)

            if save:
                im_path = path / f"{count}.jpg"
                clean_im_path = path / f"{count}_clean.jpg"
                rot_im_path = path / f"{count}_rot.jpg"
                txt_path = path / f"{count}.txt"
                im = Image.fromarray(crop["im"])
                clean_img = Image.fromarray(clean_img)
                rot = Image.fromarray(rot)
                im.save(im_path)
                clean_img.save(clean_im_path)
                rot.save(rot_im_path)
                with open(txt_path, "w") as f:
                    f.write(label_text)

    save_results(boxes)

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
    with open("results.json", "w") as outfile:
        outfile.write(json_object)

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

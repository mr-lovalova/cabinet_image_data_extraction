import os
from PIL import Image
from collections import namedtuple
from pathlib import Path

ImageInfo = namedtuple("ImageInfo", "img, box location")


def image_walk(path, num=100):
    tree = os.walk(path, topdown=False)
    images = []
    for root, _, files in tree:
        for file in files:
            if file.lower().endswith("jpg"):
                location = Path(f"{root}/{file}")
                img = Image.open(location)
                box = root.split("/")[-1]
                if img is not None:
                    images.append(
                        ImageInfo(
                            img,
                            box,
                            location,
                        )
                    )
        if len(images) > num and num > 0:
            break
    return images

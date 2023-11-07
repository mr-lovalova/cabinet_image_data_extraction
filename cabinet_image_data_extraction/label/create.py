from .labels import factory
from .extract.text import extract_text, process_label2
from .process.process import process, process2
from label.text import parsing


def do_logging(og_img, processed, text, found, **ignored):
    logger = ignored["logger"]
    logger.add(og_img, "crop", found)
    logger.add(processed, "clean", found)
    logger.add(text, "text", found)


def label(image, **ignored):
    img = process(image)
    resolution = img.shape[0] * img.shape[1]
    text = extract_text(img)
    format_ = parsing.get_format(text)

    do_logging(image, img, text, found=bool(format_), **ignored)

    if not format_:
        return None
    parser = parsing.factory.get(format_)
    id_ = parser.extract_id(text)
    parsed = parser.parse(parser.remainder)
    label = factory.create(format_)
    label = label(id_, resolution, parsed=parsed)
    label.img, label.clean_img, label.blur, label.text = image, img, img, text
    return label

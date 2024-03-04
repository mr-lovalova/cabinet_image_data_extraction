from .labels import factory
from .process.clean import process
from .process.rotation import is_possibly_upside_down
from .process.rotation import rotate
from label.text.parser import parsing
from label.text.extraction import extract


def builder(crop, box, **ignored):
    clean = process(crop)
    text = extract(clean)
    format_ = parsing.get_format(text, box.station_id)

    is_180 = is_possibly_upside_down(clean)
    if format_ is None:
        clean = rotate(clean, 180)
        text = extract(clean)
        format_ = parsing.get_format(text, box.station_id)
        if format_ is None:
            clean = rotate(clean, 180)
            text = extract(clean)
    if format_ == "CONNECTION_POINT":
        if is_180:
            turned = rotate(clean, 180)
            text = extract(turned)
            format_ = parsing.get_format(text, box.station_id)
            if format_ != "CONNECTION_POINT":
                text = extract(clean)
                format_ = parsing.get_format(text, box.station_id)

    parser = parsing.factory.get(format_)
    id_ = parser.extract_id(text)

    images = {"clean": clean, "crop": crop}
    dimensions = (clean.shape[0], clean.shape[1])
    parsed = parser.parse(parser.remainder)
    label = factory.create(format_)
    label = label(
        id_, dimensions, remainder=parser.remainder, parsed=parsed, images=images
    )
    return label

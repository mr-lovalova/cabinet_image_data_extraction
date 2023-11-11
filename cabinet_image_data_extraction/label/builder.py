from .labels import factory
from .process.process import process, process2
from label.text.parser import parsing
from label.text.extraction import extract


def builder(crop, **ignored):
    clean = process(crop)
    images = {"clean": clean, "crop": crop}
    resolution = clean.shape[0] * clean.shape[1]
    
    text = extract(clean)
    format_ = parsing.get_format(text)
    parser = parsing.factory.get(format_)
    id_ = parser.extract_id(text)
    parsed = parser.parse(parser.remainder)
    label = factory.create(format_)
    label = label(
        id_, resolution, remainder=parser.remainder, parsed=parsed, images=images
    )
    return label

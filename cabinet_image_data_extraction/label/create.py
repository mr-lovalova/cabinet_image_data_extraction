from .labels import factory
from .extract.text import extract_text, process_label2
from label.text import parsing


def label(image, **_ignored):
    clean_img, rot, t_img = process_label2(image)
    # text = extract_text(clean_img) # TODO bedst med eller uden blur ? clean_img, vs text_img
    resolution = clean_img.shape[0] * clean_img.shape[1]
    text = extract_text(t_img)
    format_ = parsing.get_format(text)
    if not format_:
        return None
    parser = parsing.factory.get(format_)
    id_ = parser.extract_id(text)
    parsed = parser.parse(parser.remainder)
    label = factory.create(format_)
    return label(id_, resolution, parsed=parsed)

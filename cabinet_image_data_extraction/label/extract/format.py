import re

identifyers = {
    # all
    "STIKSKILT": re.compile(r"6\d{7}"),
    # city
    "transformer_city": re.compile(r"T.\s?\d{1,5}\s?-\s?\d\s?-\s?\d{1,2}"),
    "DELT_SKAB": re.compile(
        r"(4|6|7)\s?D.?\s?skab\s?\d{1,5}\s?-\s?\d{1,4}", re.IGNORECASE
    ),
    # nord
    "transformer_nord": re.compile(r"T.\s?\d{1,5}\s?-\s?\d\s?-\s?[A-ZÅÆØ]"),
    # all
    "STRÆKNINGSSKILT": re.compile(
        r"^(Skab|SKAB)\s?\d{1,5}\s?-\s?\d{1,4}"  # TODO r"Skab\s?\d{1,5}\s?-\s?\d{1,4}" differentier mlm. ukorrekt ndelt og strækningskilt
    ),  # TODO hvor mange digits efter bindestreg? # TODO Kan man adskille udføringsskab og strækningsskab? # TODO blandes sammen med delte skabe
}


def get_format(text):
    """get label format"""
    for format_, pattern in identifyers.items():
        match = re.search(pattern, text)
        if match:
            return format_
    return None


def get_id(text, format_):
    """get label ID"""
    match = re.search(identifyers[format_], text)
    return match.group()


def get_remainder(text, id_):
    """get remainding text"""
    split = text.split(id_, 1)
    return split[-1]


def extract_id(text):
    format_ = get_format(text)
    if format_:
        id_ = get_id(text, format_)
        remainder = get_remainder(text, id_)
        return format_, id_, remainder
    return None

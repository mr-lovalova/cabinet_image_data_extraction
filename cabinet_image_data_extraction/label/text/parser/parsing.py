import re
import sys
from helpers import merge, ObjectFactory
from .parser import LabelParser

sys.path.append("....")
from main import parse_id

identifyers = {
    # all
    "CONNECTION_POINT": re.compile(r"6\d{7}"),
}

dimension = {"dimension": re.compile(r"\dx\d{2,3}(mm|mm2)?\s?(cu|al)", re.IGNORECASE)}
ampere = {"ampere": re.compile(r"\d{2}\s?A$")}
address = {
    "address": re.compile(
        r"([A-ZÅÆØ][a-zæøå]{2,}(.|\s))?[A-ZÅÆØ]?[a-zæøå]{2,}\s\d{1,3}(-\d{0,3})?"
    )
}


def get_format(text, station_id=None):
    """get label format"""
    identifyers["SUBSECTION"] = re.compile(
        station_id + r"\s?-\s?(?!0$)\d{0,5}",
        re.IGNORECASE,
    )
    for format_, pattern in identifyers.items():
        match = re.search(pattern, text)
        if match:
            return format_
    return None


class ConnectionPointLabelParser(LabelParser):
    @property
    def _id_pattern(self):
        return identifyers["CONNECTION_POINT"]

    @property
    def _patterns(self):
        return merge(dimension, address, ampere)  # merge(dimension, ampere, address)?


class SubSectionLabelParser(LabelParser):
    @property
    def _id_pattern(self):
        return identifyers["SUBSECTION"]

    @property
    def _patterns(self):
        return {}

    def _correct_format(self, id_):
        id_ = parse_id(id_)
        return id_


class UnknownLabelParser(LabelParser):
    @property
    def _id_pattern(self):
        pass

    @property
    def _patterns(self):
        return merge(dimension, ampere, address)

    def extract_id(self, text):
        self.remainder = text
        return None


class ParserProvider(ObjectFactory):
    def get(self, format_, **kwargs):
        return self.create(format_, **kwargs)

    def register_format(self, format_, pattern):
        self.register_builder(format_, pattern)


factory = ParserProvider()
factory.register_format("CONNECTION_POINT", ConnectionPointLabelParser)
factory.register_format("SUBSECTION", SubSectionLabelParser)
factory.register_format(None, UnknownLabelParser)

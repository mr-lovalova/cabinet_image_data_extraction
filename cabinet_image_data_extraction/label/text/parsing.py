import re
from helpers import merge, ObjectFactory
from .parser import LabelParser

5 - 24
identifyers = {
    # all
    "STIKSKILT": re.compile(r"6\d{7}"),
    # city
    "DELT_SKAB": re.compile(
        r"(4|6|7)\s?D.?\s?skab\s?\d{1,5}\s?-\s?\d{1,4}", re.IGNORECASE
    ),
    # all
    "STRÆKNINGSSKILT": re.compile(
        r"^(skab)\s?\d{1,5}\s?-\s?\d{1,4}",
        re.IGNORECASE,  # TODO r"Skab\s?\d{1,5}\s?-\s?\d{1,4}" differentier mlm. ukorrekt ndelt og strækningskilt
    ),  # TODO hvor mange digits efter bindestreg? # TODO Kan man adskille udføringsskab og strækningsskab? # TODO blandes sammen med delte skabe
}

later = {
    "transformer_nord": re.compile(r"T.\s?\d{1,5}\s?-\s?\d\s?-\s?[A-ZÅÆØ]"),
    "transformer_city": re.compile(r"T.\s?\d{1,5}\s?-\s?\d\s?-\s?\d{1,2}"),
}

dimension = {
    "dimension": re.compile(r"\dx\d{2,3}(mm|mm2)?\s?(cu|al)", re.IGNORECASE)
}  # TODO mm2?? or mm
ampere = {"ampere": re.compile(r"\d{2,3}\s?A")}
address = {
    "address": re.compile(r"[A-ZÅÆØ][a-zæøå]{2,}\s\d{1,3}(-\d{0,3})?")
}  # TODO include multiword address, with and without . e.g. Sdr. Bouleward


def get_format(text):
    """get label format"""
    for format_, pattern in identifyers.items():
        match = re.search(pattern, text)
        if match:
            return format_
    return None


class StikSkiltParser(LabelParser):
    @property
    def _id_pattern(self):
        return identifyers["STIKSKILT"]

    @property
    def _patterns(self):
        return merge(dimension, address, ampere)  # merge(dimension, ampere, address)?


class StrækningSkiltParser(LabelParser):
    @property
    def _id_pattern(self):
        return identifyers["STRÆKNINGSSKILT"]

    @property
    def _patterns(self):
        return {}


class DeltSkabParser(LabelParser):
    @property
    def _id_pattern(self):
        return identifyers["DELT_SKAB"]

    @property
    def _patterns(self):
        return merge(dimension, ampere, address)


class ParserProvider(ObjectFactory):
    def get(self, format_, **kwargs):
        return self.create(format_, **kwargs)

    def register_format(self, format_, pattern):
        self.register_builder(format_, pattern)


factory = ParserProvider()
factory.register_format("STIKSKILT", StikSkiltParser)
factory.register_format("STRÆKNINGSSKILT", StrækningSkiltParser)
factory.register_format("DELT_SKAB", DeltSkabParser)

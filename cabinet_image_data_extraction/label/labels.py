import re
from abc import ABC, abstractmethod
from helpers import ObjectFactory
from item import Item


class Label(Item):
    def __init__(self, id_, resolution):
        self.id = id_
        self.resolution = resolution

    @property
    @abstractmethod
    def type(self):
        pass

    def __eq__(self, other):
        return self.id == other.id

    def __gt__(self, other):
        """used as naive guess of most reliable output"""
        return self.resolution > other.resolution

    def __hash__(self):
        return hash(self.id)

    def asdict(self):
        out = dict(vars(self))
        out.pop("id")
        out.pop("resolution")
        return out


class StikSkilt(Label):
    def __init__(self, id_, resolution, parsed):
        super().__init__(id_, resolution)
        self.address = parsed.get("address", None)
        self.ampere = parsed.get("ampere", None)
        self.dimension = parsed.get("dimension", None)

    @property
    def type(self):
        return "STIKSKILT"


class StikSkiltBuilder:
    def __call__(self, id_, resolution, parsed, **_ignored):
        return StikSkilt(id_, resolution, parsed)


class StrækningsSkilt(Label):
    def __init__(self, id_, resolution):
        super().__init__(id_, resolution)

    @property
    def type(self):
        return "STRÆKNINGSSKILT"


class StrækningsSkiltBuilder:
    def __call__(self, id_, resolution, **_ignored):
        return StrækningsSkilt(id_, resolution)


class DeltSkab(Label):
    def __init__(self, id_, resolution, parsed):
        super().__init__(id_, resolution)
        self.address = parsed.get("address", None)
        self.ampere = parsed.get("ampere", None)
        self.dimension = parsed.get("dimension", None)
        # antal delinger e.g. 7 d
        # inherit from skab?

    @property
    def type(self):
        return "DELT_SKAB"


class DeltSkabBuilder:
    def __call__(self, id_, resolution, parsed, **_ignored):
        return StikSkilt(id_, resolution, parsed)


factory = ObjectFactory()
factory.register_builder("STIKSKILT", StikSkiltBuilder)
factory.register_builder("STRÆKNINGSSKILT", StrækningsSkiltBuilder)
factory.register_builder("DELT_SKAB", DeltSkabBuilder)

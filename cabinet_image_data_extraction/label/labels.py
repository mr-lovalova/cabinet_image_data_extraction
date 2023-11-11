from abc import abstractmethod
from helpers import ObjectFactory
from item import Item


class Label(Item):
    def __init__(self, id_, resolution, remainder, **images):
        self.id = id_
        self.resolution = resolution
        self.imgs = images
        self.remainder = remainder

    @property
    def type(self):
        return "LABEL"

    @property
    @abstractmethod
    def format(self):
        pass

    @property
    def is_valid(self):
        return bool(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __gt__(self, other):
        """used as naive guess of most reliable output"""
        return self.resolution > other.resolution

    def __repr__(self):
        out = dict(vars(self))
        out["format"] = self.format
        out.pop("imgs")
        out.pop("remainder")
        return str(out)

    def __hash__(self):
        return hash(self.id)


class StikSkilt(Label):
    def __init__(self, id_, resolution, remainder, parsed, **images):
        super().__init__(id_, resolution, remainder, **images)
        self.address = parsed.get("address", None)
        self.ampere = parsed.get("ampere", None)
        self.dimension = parsed.get("dimension", None)

    @property
    def format(self):
        return "STIKSKILT"


class StikSkiltBuilder:
    def __call__(self, id_, resolution, remainder, parsed, images, **_ignored):
        return StikSkilt(id_, resolution, remainder, parsed, **images)


class StrækningsSkilt(Label):
    @property
    def format(self):
        return "STRÆKNINGSSKILT"


class StrækningsSkiltBuilder:
    def __call__(self, id_, resolution, remainder, images, **_ignored):
        return StrækningsSkilt(id_, resolution, remainder, **images)


class DeltSkab(Label):
    def __init__(self, id_, resolution, remainder, parsed, **images):
        super().__init__(id_, resolution, remainder**images)
        self.address = parsed.get("address", None)
        self.ampere = parsed.get("ampere", None)
        self.dimension = parsed.get("dimension", None)
        # antal delinger e.g. 7 d
        # inherit from skab?

    @property
    def format(self):
        return "DELT_SKAB"


class DeltSkabBuilder:
    def __call__(self, id_, resolution, parsed, images, **_ignored):
        return StikSkilt(id_, resolution, parsed, **images)


class UnknownLabel(Label):
    @property
    def format(self):
        return "UNKNOWN"

    def __hash__(self):
        return hash(self.id_, self.resolution, self.remainder)


class UnknownLabelBuilder:
    def __call__(self, id_, resolution, remainder, images, **_ignored):
        return UnknownLabel(id_, resolution, remainder, **images)


factory = ObjectFactory()
factory.register_builder("STIKSKILT", StikSkiltBuilder)
factory.register_builder("STRÆKNINGSSKILT", StrækningsSkiltBuilder)
factory.register_builder("DELT_SKAB", DeltSkabBuilder)

factory.register_builder(None, UnknownLabelBuilder)

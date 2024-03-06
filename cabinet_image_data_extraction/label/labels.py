from abc import abstractmethod
from helpers import ObjectFactory
from .model import Label


class ConnectionPoint(Label):
    def __init__(self, id_, resolution, remainder, parsed, **images):
        super().__init__(id_, resolution, remainder, **images)
        self.address = parsed.get("address", None)
        self.ampere = parsed.get("ampere", None)
        self.dimension = parsed.get("dimension", None)

    @property
    def format(self):
        return "CONNECTION_POINT"

    def serialize(self, serializer):
        super().serialize(serializer)
        serializer.add_property("ampere", self.ampere)
        serializer.add_property("dimension", self.dimension)
        serializer.add_property("address", self.address)


class ConnectionPointBuilder:
    def __call__(self, id_, resolution, remainder, parsed, images, **_ignored):
        return ConnectionPoint(id_, resolution, remainder, parsed, **images)


class SubSection(Label):
    @property
    def format(self):
        return "SUBSECTION"


class SubSectionBuilder:
    def __call__(self, id_, resolution, remainder, images, **_ignored):
        return SubSection(id_, resolution, remainder, **images)


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
factory.register_builder("CONNECTION_POINT", ConnectionPointBuilder)
factory.register_builder("SUBSECTION", SubSectionBuilder)

factory.register_builder(None, UnknownLabelBuilder)

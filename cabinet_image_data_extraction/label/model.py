from abc import abstractmethod
from item.model import Object


class Label(Object):
    def __init__(self, id_, dimensions, remainder, **images):
        self.id = id_
        self.dimensions = dimensions
        self.resolution = dimensions[0] * dimensions[1]
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

    def serialize(self, serializer):
        serializer.start_object("id", self.id)
        serializer.add_property("format", self.format)

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
        out.pop("dimensions")
        return str(out)

    def __hash__(self):
        return hash(self.id)

from abc import abstractmethod
from item.model import Model


class Label(Model):
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

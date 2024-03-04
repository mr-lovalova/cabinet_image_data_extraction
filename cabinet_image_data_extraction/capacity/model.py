from item.model import Object


class Capacity(Object):
    def __init__(self, capacity):
        self.capactiy = capacity

    @property
    def type(self):
        return "CAPACITY"

    def is_valid(self):
        """should extracted information be kept or is bad quality e.g. labels with no id"""
        return True

    def __gt__(self, other):
        pass

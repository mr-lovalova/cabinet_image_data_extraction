from abc import ABC, abstractmethod


class Item(ABC):
    @property
    @abstractmethod
    def type(self):
        pass

    @property
    @abstractmethod
    def is_valid(self):
        """should extracted information be kept or is bad quality e.g. labels with no id"""
        pass

    @abstractmethod
    def __gt__(self, other):
        pass

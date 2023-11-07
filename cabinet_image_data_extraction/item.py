from abc import ABC, abstractmethod


class Item(ABC):
    @property
    @abstractmethod
    def type(self):
        pass

    @abstractmethod
    def __gt__(self, other):
        pass


class InsideItem(Item):
    # for all things inside the cabinet???
    @abstractmethod
    def __gt__(self, other):
        pass

    @abstractmethod
    def log(self):
        pass

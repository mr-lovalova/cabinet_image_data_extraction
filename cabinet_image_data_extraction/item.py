from abc import ABC, abstractmethod


class Item(ABC):
    @property
    @abstractmethod
    def type(self):
        pass

    @abstractmethod
    def asdict(self):
        pass

    @abstractmethod
    def __gt__(self, other):
        pass

from abc import ABC, abstractmethod
from helpers import ObjectFactory
from label import create


# all objects should inheret from Item class
factory = ObjectFactory()
factory.register_builder("black", create.label)

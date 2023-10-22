from helpers import ObjectFactory
from label import create


factory = ObjectFactory()
factory.register_builder("black", create.label)

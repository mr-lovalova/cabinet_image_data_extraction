import label
import capacity
import cabinet_model
from .skip import skip
from helpers import ObjectFactory


# factories for item-detections
factory = ObjectFactory()
factory.register_builder("black", label.builder)
factory.register_builder("old", skip)
factory.register_builder("yellow", skip)
factory.register_builder("cabinet_model", cabinet_model.builder)
factory.register_builder("capacity", capacity.builder)

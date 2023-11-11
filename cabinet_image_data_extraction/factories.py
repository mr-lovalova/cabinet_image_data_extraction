import label
import capacity
import cabinet_model
from helpers import ObjectFactory
from item import Item


class Skip(Item):
    @property
    def type(self):
        return "SKIP"

    @property
    def is_valid(self):
        """should extracted information be kept or is bad quality e.g. labels with no id"""
        return False

    def __gt__(self, other):
        pass


def skip(**ignored):
    return Skip()


# factories for item-detections
item = ObjectFactory()
item.register_builder("black", label.builder)
item.register_builder("old", skip)
item.register_builder("yellow", skip)
item.register_builder("cabinet_model", cabinet_model.builder)
item.register_builder("capacity", capacity.builder)

logger = ObjectFactory()
# logger.register_format("JSON", JsonSerializer)
# logger.register_format("XML", XmlSerializer)

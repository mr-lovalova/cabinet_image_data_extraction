from label import create
from helpers import ObjectFactory


item = ObjectFactory()
item.register_builder("black", create.label)

logger = ObjectFactory()
# logger.register_format("JSON", JsonSerializer)
# logger.register_format("XML", XmlSerializer)

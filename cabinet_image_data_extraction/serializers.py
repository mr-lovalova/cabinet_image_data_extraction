import json
from helpers import ObjectFactory
from abc import ABC, abstractmethod


class ObjectSerializer:
    def serialize(self, serializable, format_):
        serializer = factory.create(format_)
        serializable.serialize(serializer)
        return serializer.to_str()


class Serializer(ABC):
    def __init__(self):
        self._current_object = None

    @abstractmethod
    def start_object(self, object_name, object_id):
        self._current_object = {"id": object_id}

    @abstractmethod
    def add_property(self, name, value):
        self._current_object[name] = value

    @abstractmethod
    def to_str(self):
        return self._current_object


class DictSerializer(Serializer):
    def start_object(self, object_name, object_id):
        self._current_object = {"id": object_id}

    def add_property(self, name, value):
        self._current_object[name] = value

    def to_str(self):
        return self._current_object


class JsonSerializer(DictSerializer):
    def to_str(self):
        return json.dumps(super().to_str())


factory = ObjectFactory()
factory.register_builder("DICT", DictSerializer)
factory.register_builder("JSON", JsonSerializer)
serializer = ObjectSerializer()

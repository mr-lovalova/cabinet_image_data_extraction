from pathlib import Path
from PIL import Image
from helpers import ObjectFactory
from abc import abstractmethod, ABC
from helpers import ObjectFactory
import os


class Logger:
    def __init__(self, destination=None, verbose_lvl=1):
        self.dest = destination
        self.verbose = verbose_lvl
        self.boxes = 0
        self.current = None

    def start(self, id_) -> None:
        self.current = id_
        self.boxes += self.boxes

    def log(self, item):
        path = f"{self.dest}{item.type}/{self.current}/"
        logger = loggers.create(item.type)
        logger.start(item=item)
        logger.save(path=path)
        print(logger.output())


class LabelLogger:
    def __init__(self):
        self.label = None

    def start(self, item, **ignored):
        self.label = item

    def save(self, path, **ignored):
        destination = self._get_destination(path)

        file = self._create_file(destination, "text", "txt")
        with open(file, "w") as f:
            f.write(str(self.label))

        for type_, img in self.label.imgs.items():
            file = self._create_file(destination, type_, "jpg")
            Image.fromarray(img).save(file)

    def _create_file(self, destination, name, extension):
        file = destination + f"/{name}.{extension}"
        count = 0
        while os.path.isfile(file):
            count += 1
            file = destination + f"/{count}_{name}.{extension}"

        return file

    def _get_destination(self, path):
        if self.label.is_valid:
            folder = str(self.label.id)
        else:
            folder = "UNIDENTIFIED"

        destination = path + folder
        self._ensure_path(destination)
        return destination

    def _ensure_path(self, path):
        Path(path).mkdir(parents=True, exist_ok=True)

    def output(self, **ignored):
        return str(self.label)


class SkipLogger:
    def start(self, **ignored):
        pass

    def save(self, **ignored):
        pass

    def output(self, **ignored):
        pass


loggers = ObjectFactory()
loggers.register_builder("LABEL", LabelLogger)
loggers.register_builder("SKIP", SkipLogger)

from pathlib import Path
from PIL import Image
from helpers import ObjectFactory


# implement as with factories instead of this yikes


class Logger:
    total_boxes = 0
    total_imgs = 0
    detected_labels = 0
    extracted_labels = 0

    def __init__(self, folder, id_):
        self.destination = folder
        self.id = id_
        self.found = {}
        self.not_found = {}
        Logger.total_boxes += 1

    def add(self, item, type_, found):
        if found:
            if type_ not in self.found:
                self.found[type_] = []
            self.found[type_].append(item)
        else:
            if type_ not in self.not_found:
                self.not_found[type_] = []
            self.not_found[type_].append(item)

    def log(self):
        box_count_str = f"{Logger.total_boxes} boxes searched"
        img_count_str = f"{Logger.total_imgs} images searched"
        labels_count_str = f"{Logger.detected_labels} labels detected"
        labels_extracted_count_str = f"{Logger.extracted_labels} labels extracted"
        print(
            f"BOX: {self.id} \n {box_count_str} \n {img_count_str} \n {labels_count_str} \n {labels_extracted_count_str}"
        )

    def _create_folders(self):
        found, not_found = self._get_destination_strs()
        if len(self.found):
            Path(found).mkdir(parents=True, exist_ok=True)
        if len(self.not_found):
            Path(not_found).mkdir(parents=True, exist_ok=True)

    def _get_destination_strs(self):
        found_path = self.destination + "found/" + self.id + "/"
        not_found_path = self.destination + "not_found/" + self.id + "/"
        return found_path, not_found_path

    def save(self):
        self._create_folders()
        found_path, not_found_path = self._get_destination_strs()

        for item in self.found.items():
            key, lst = item
            for count, value in enumerate(lst):
                if isinstance(value, str):
                    path = found_path + f"{str(count)}.txt"
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(value)
                else:
                    path = found_path + f"{str(count)}{key}.jpg"
                    Image.fromarray(value).save(path)

        for item in self.not_found.items():
            key, lst = item
            for count, value in enumerate(lst):
                if isinstance(value, str):
                    path = not_found_path + f"{str(count)}.txt"
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(value)
                else:
                    path = not_found_path + f"{str(count)}{key}.jpg"
                    Image.fromarray(value).save(path)

    def log2(self, logable, format_):
        folder, id_
        # Logable: box, image, text etc. ?
        logger = factory.create(format_)
        logable.log(logger)
        return logger.to_str()

    # add abstract log method to all items? and box?


    def serialize(self, serializer, folder, id_):
        serializer.start_object('song', self.song_id)
        serializer.add_property('title', self.title)
        serializer.add_property('artist', self.artist)

class ImgLogger:
    def __init__(self):
        self._img = None

    def ensure_path(self, object_name, object_id):
        #self._element = et.Element(object_name, attrib={'id': object_id})
        pass

    def add_property(self, name, value):
        # prop = et.SubElement(self._element, name)
        # prop.text = value
        pass

    def to_str(self):
        pass
        # return et.tostring(self._element, encoding='unicode')

class TextLogger:
    def __init__(self):
        self._element = None

    def start_object(self, object_name, object_id):
        #self._element = et.Element(object_name, attrib={'id': object_id})
        pass

    def add_property(self, name, value):
        # prop = et.SubElement(self._element, name)
        # prop.text = value
        pass

    def to_str(self):
        pass
        # return et.tostring(self._element, encoding='unicode')

factory = ObjectFactory()
# factory.register_format("JSON", JsonSerializer)
# factory.register_format("XML", XmlSerializer)

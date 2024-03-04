from serializers import ObjectSerializer


class Box:
    """Data structure to represent electrical cabinet"""

    def __init__(self, id_) -> None:
        self.id = id_
        self.labels = []
        self.station_id, self.cabinet_number = id_.split("-")
        self.model = None
        self.capacity = []

    def add_object(self, item):
        # TODO change to factory style before adding more capacity, model etc.
        if item.type == "LABEL":
            if item not in self.labels:
                self.labels.append(item)
            else:
                # check which item to keep
                idx = self.labels.index(item)
                old_item = self.labels[idx]
                if item > old_item:
                    self.labels.pop(idx)
                    self.labels.append(item)
        elif item.type == "CAPACTITY":
            self.capacity.append(item)
        else:
            raise NotImplementedError(item.type, " type has not been implemented yet")

    def serialize(self, serializer):
        serialized = []
        for label in self.labels:
            s = ObjectSerializer()
            serialized.append(s.serialize(label, "DICT"))

        serializer.start_object("id", self.id)
        serializer.add_property("labels", serialized)

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return f"BOX:{self.id}"

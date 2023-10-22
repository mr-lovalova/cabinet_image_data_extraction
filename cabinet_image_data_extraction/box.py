class Box:
    """"""

    def __init__(self, id_) -> None:
        self.id = id_
        self.items = {}

    def add(self, item, type_):
        if type_ not in self.items:
            self.items[type_] = {}
        if item not in self.items[type_]:
            self.items[type_][item.id] = item
        else:
            old_item = self.items[type_][item.id]
            if item > old_item:
                self.items[type_][item.id] = item

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return f"BOX:{self.id}, {self.labels}"

    def __repr__(self):
        return f"{self.id}"

    def __iter__(self):
        for key in self.__dict__:
            if key == "id":
                continue
            yield key, getattr(self, key)

    def asdict(self):
        labels = {}
        for k, v in self.labels.items():
            labels[k] = {}
            for l in v.values():
                labels[k][l.id] = l.asdict()
        return labels

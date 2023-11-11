class Box:
    """"""

    def __init__(self, id_) -> None:
        self.id = id_
        # self.items = {}
        self.labels = []
        self.model = None
        self.capacity = None

    def add(self, item):
        # instad of this shit
        # change to factory style before adding more capacity, model etc.
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
        else:
            raise NotImplementedError(item.type, " type has not been implemented yet")

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return f"BOX:{self.id}"

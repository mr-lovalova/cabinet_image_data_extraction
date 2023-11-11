from .model import Model


class Skip(Model):
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

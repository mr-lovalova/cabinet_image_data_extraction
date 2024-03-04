from abc import ABC, abstractmethod
import re

from .filters import filters
from .mappings import mappings


class LabelParser(ABC):
    def __init__(self):
        self.parsed = {}
        self.remainder = None

    @property
    @abstractmethod
    def _patterns(self):
        pass

    @property
    @abstractmethod
    def _id_pattern(self):
        pass

    def _correct_format(self, id_):
        """used in strækningskilt to remomve leading zeros for example"""
        return id_

    def _clean_id(self, id_):
        id_ = "".join(filter(lambda x: x.isnumeric() or x == "-", id_))
        id_ = self._correct_format(id_)
        return id_

    def parse(self, text):
        self.remainder = text
        for key, regex in self._patterns.items():
            extracted = self._extract(regex, self.remainder)
            if extracted:
                extracted = self._clean_extracted(key, extracted.group(0))
            self.parsed[key] = extracted
        return self.parsed

    def _extract(self, regex, text):
        """takes a pattern and adds it to parsed if it is present"""
        match_ = re.search(regex, text)
        if match_:
            self.remainder = self._get_remainder(text, match_.group(0))
        return match_

    def extract_id(self, text):
        """get label ID which should be extracted before anything else to make sure we get it right"""
        id_ = self._extract(self._id_pattern, text)
        id_ = self._clean_id(id_.group(0))
        return id_

    def _get_remainder(self, text, remove):
        """get remainding text"""
        return text.replace(remove, "", 1)

    def _clean_extracted(self, key, replacement):
        """Filters unwanted signs and maps to shared format"""
        cleaned = filter(filters[key], enumerate(replacement))
        cleaned = map(mappings[key], cleaned)
        cleaned = "".join(cleaned)
        return cleaned

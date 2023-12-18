from logging import Filterer as _Filterer
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nlogging.records import LogRecord

    from .filter import Filter


class Filterer(_Filterer):
    if TYPE_CHECKING:
        filters: dict[str, "Filter"]

    def __init__(self):
        self.filters = dict()

    def addFilter(self, filter: "Filter"):
        self._validate_filter(filter)

        if filter.id not in self.filters:
            self.filters[filter.id] = filter

    def removeFilter(self, filter: "Filter"):
        self._validate_filter(filter)
        self.filters.pop(filter.id, None)

    def filter(self, record: "LogRecord"):
        for key in self.filters:
            if not self.filters[key].filter(record):
                return False
        return True

    def _validate_filter(self, filter: "Filter"):
        if not hasattr(filter, "id"):
            raise TypeError("Filter must have an id attribute")

        if not isinstance(filter.id, str):
            raise TypeError("Filter id must be a string")

        if not hasattr(filter, "filter"):
            raise TypeError("Filter must have a filter method")

        if not callable(filter.filter):
            raise TypeError("Filter filter method must be callable")

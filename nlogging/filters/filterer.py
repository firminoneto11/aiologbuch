from logging import Filterer as _Filterer
from typing import TYPE_CHECKING

from .filter import Filter

if TYPE_CHECKING:
    from nlogging.records import LogRecord


class Filterer(_Filterer):
    if TYPE_CHECKING:
        filters: dict[str, Filter]

    def __init__(self):
        self.filters = dict()

    def addFilter(self, filter: Filter):
        self._validate_filter(filter)

        if filter.id not in self.filters:
            self.filters[filter.id] = filter

    def removeFilter(self, filter: Filter):
        self._validate_filter(filter)
        self.filters.pop(filter.id, None)

    def filter(self, record: "LogRecord"):
        for key in self.filters:
            if not self.filters[key].filter(record):
                return False
        return True

    def _validate_filter(self, filter: Filter):
        if not isinstance(filter, Filter):
            raise TypeError("filter must be an instance of Filter")

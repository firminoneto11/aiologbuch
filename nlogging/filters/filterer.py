from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nlogging.records import LogRecord

    from .filter import Filter


class Filterer:
    if TYPE_CHECKING:
        filters: dict[str, "Filter"]

    def __init__(self):
        self.filters = dict()

    def add_filter(self, filter: "Filter"):
        self._validate_filter(filter=filter, adding=True)

        if filter.id not in self.filters:
            self.filters[filter.id] = filter

    def remove_filter(self, filter: "Filter"):
        self._validate_filter(filter)
        self.filters.pop(filter.id, None)

    def filter(self, record: "LogRecord"):
        for ft in self.filters.values():
            if not ft.filter(record):
                return False
        return True

    def _validate_filter(self, filter: "Filter", adding: bool = False):
        if not hasattr(filter, "id"):
            raise TypeError("Filter must have an id attribute")

        if (adding) and (not hasattr(filter, "filter")):
            raise TypeError("Filter must have a filter method")

from functools import lru_cache
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from logging import LogRecord


@lru_cache(maxsize=1)
def _filter_id_generator():
    i = 1
    while True:
        yield i
        i += 1


class Filter:
    def __init__(self, level: int):
        self._level = level
        self._id = next(_filter_id_generator())

    @property
    def id(self):
        return self._id

    @property
    def level(self):
        return self._level

    def filter(self, record: "LogRecord"):
        return record.levelno >= self._level

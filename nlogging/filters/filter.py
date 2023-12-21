from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from logging import LogRecord


def _filter_id_generator():
    i = 1
    while True:
        yield str(i)
        i += 1


class Filter:
    def __init__(self, level: int):
        self._level = level
        self._id = next(_filter_id_generator())

    @property
    def id(self):
        return self._id

    def filter(self, record: "LogRecord"):
        return record.levelno >= self._level

from logging import Filter as LoggingFilter
from typing import TYPE_CHECKING
from uuid import uuid4

if TYPE_CHECKING:
    from nlogging.records import LogRecord


class Filter(LoggingFilter):
    def __init__(self, level: int):
        self._level = level
        self._id = uuid4().hex

    @property
    def id(self):
        return self._id

    def filter(self, record: "LogRecord"):
        return self._level == record.levelno

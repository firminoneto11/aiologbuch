from typing import TYPE_CHECKING

from nlogging.levels import check_level

if TYPE_CHECKING:
    from logging import LogRecord

    from nlogging._types import LevelType


class Filter:
    def __init__(self, level: "LevelType"):
        self._level = check_level(level)

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value: "LevelType"):
        self._level = check_level(value)

    def filter(self, record: "LogRecord"):
        return record.levelno >= self.level


class ExclusiveFilter(Filter):
    def filter(self, record: "LogRecord"):
        return record.levelno == self.level

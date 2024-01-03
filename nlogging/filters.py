from dataclasses import dataclass
from logging import LogRecord


@dataclass
class Filter:
    level: int

    def filter(self, record: LogRecord):
        return record.levelno >= self.level


@dataclass
class ExclusiveFilter:
    level: int

    def filter(self, record: LogRecord):
        return record.levelno == self.level

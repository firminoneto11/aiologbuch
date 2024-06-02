from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from logging._types import LogRecordProtocol


class Filter:
    def __init__(self, level: int):
        self._level = level

    @property
    def level(self):
        return self._level

    def filter(self, record: "LogRecordProtocol | int"):
        if isinstance(record, int):
            return record >= self.level
        return record.levelno >= self.level


class ExclusiveFilter(Filter):
    def filter(self, record: "LogRecordProtocol | int"):
        if isinstance(record, int):
            return record == self.level
        return record.levelno == self.level

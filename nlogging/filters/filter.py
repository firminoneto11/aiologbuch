from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from logging import LogRecord


class Filter:
    def __init__(self, level: int):
        self._level = level

    def filter(self, record: "LogRecord"):
        return self._level == record.levelno

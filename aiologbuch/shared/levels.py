import logging
from enum import IntEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aiologbuch.shared.types import LevelType


class LogLevel(IntEnum):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


def check_level(level: "LevelType"):
    if isinstance(level, int):
        if level not in _LEVEL_TO_NAME:
            raise ValueError(f"Unknown level: {level}")
        return level
    elif isinstance(level, str):
        try:
            return _NAME_TO_LEVEL[level.upper().strip()]
        except KeyError:
            raise ValueError(f"Unknown level: {level}")
    else:
        raise TypeError(f"Level not an union of int and str: {level}")


_NAME_TO_LEVEL = {level: LogLevel[level].value for level in LogLevel.__members__}

_LEVEL_TO_NAME = {level.value: level.name for level in LogLevel}

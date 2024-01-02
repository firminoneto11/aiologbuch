import logging
from enum import IntEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nlogging._types import LevelType


class LogLevel(IntEnum):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL
    NOTSET = logging.NOTSET


NAME_TO_LEVEL = {level: LogLevel[level].value for level in LogLevel.__members__}

LEVEL_TO_NAME = {level.value: level.name for level in LogLevel}


def get_level_name(level: int):
    try:
        return LEVEL_TO_NAME[level]
    except KeyError as exc:
        raise ValueError(f"Unknown level name: {level}") from exc


def check_level(level: "LevelType"):
    if isinstance(level, int):
        if level not in LEVEL_TO_NAME:
            raise ValueError(f"Unknown level: {level}")
        return level
    elif isinstance(level, str):
        try:
            return NAME_TO_LEVEL[level.upper().strip()]
        except KeyError:
            raise ValueError(f"Unknown level: {level}")
    else:
        raise TypeError(f"Level not an union of int and str: {level}")

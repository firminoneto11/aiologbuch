from logging.filters import Filter
from logging.levels import LogLevel
from unittest.mock import MagicMock

from pytest import mark


@mark.unit
@mark.parametrize(
    "filter_level,record_level,expected",
    [
        (LogLevel.DEBUG, LogLevel.DEBUG, True),
        (LogLevel.INFO, LogLevel.DEBUG, False),
        (LogLevel.INFO, LogLevel.WARNING, True),
        (LogLevel.WARNING, LogLevel.INFO, False),
        (LogLevel.CRITICAL, LogLevel.DEBUG, False),
    ],
)
def test_filter(filter_level: int, record_level: int, expected: bool):
    _filter = Filter(level=filter_level)
    record = MagicMock(levelno=record_level)

    assert _filter.level == filter_level
    assert _filter.filter(record) == expected

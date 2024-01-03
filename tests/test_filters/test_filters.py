from unittest.mock import MagicMock

from pytest import mark

from nlogging.filters import Filter


@mark.unit
@mark.parametrize(
    "filter_level,record_level,expected",
    [
        (10, 10, True),
        (10, 9, False),
        (10, 11, True),
        (10, 0, False),
        (5, 1, False),
    ],
)
def test_filter(filter_level: int, record_level: int, expected: bool):
    _filter = Filter(level=filter_level)
    record = MagicMock(levelno=record_level)

    assert _filter.level == filter_level
    assert _filter.filter(record) == expected

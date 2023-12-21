from dataclasses import dataclass

from pytest import mark

from nlogging.filters import Filter
from nlogging.filters.filter import _filter_id_generator


@dataclass
class MockRecord:
    levelno: int


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
    record = MockRecord(levelno=record_level)

    assert _filter.id == next(_filter_id_generator()) - 1
    assert _filter.level == filter_level
    assert _filter.filter(record) == expected


@mark.unit
def test_filter_id_generator():
    latest_id = next(_filter_id_generator())

    assert hex(id(_filter_id_generator())) == hex(id(_filter_id_generator()))
    assert next(_filter_id_generator()) == latest_id + 1
    assert next(_filter_id_generator()) == latest_id + 2
    assert next(_filter_id_generator()) == latest_id + 3

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nlogging._types import LogRecordProtocol


@dataclass
class Filter:
    level: int

    def filter(self, record: "LogRecordProtocol"):
        return record.levelno >= self.level


class ExclusiveFilter(Filter):
    def filter(self, record: "LogRecordProtocol"):
        return record.levelno == self.level

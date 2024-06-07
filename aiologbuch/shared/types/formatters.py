from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from .records import LogRecordProtocol


class FormatterProtocol(Protocol):
    def format(self, record: "LogRecordProtocol") -> bytes:
        ...

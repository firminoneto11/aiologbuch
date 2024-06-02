from typing import TYPE_CHECKING, Protocol, Self

if TYPE_CHECKING:
    from .records import LogRecordProtocol


class FilterProtocol(Protocol):
    def __call__(self, level: int) -> Self:
        ...

    def filter(self, record: "LogRecordProtocol | int") -> bool:
        ...

    @property
    def level(self) -> int:
        ...

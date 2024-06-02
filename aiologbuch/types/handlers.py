from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from .records import LogRecordProtocol


class AsyncHandlerProtocol(Protocol):
    @property
    def id(self) -> int:
        ...

    async def close(self) -> None:
        ...

    async def handle(self, record: "LogRecordProtocol") -> None:
        ...

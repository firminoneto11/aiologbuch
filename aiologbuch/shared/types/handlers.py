from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from .records import LogRecordProtocol


class AsyncHandlerProtocol(Protocol):
    async def handle(self, record: "LogRecordProtocol") -> None:
        ...

    async def close(self) -> None:
        ...


class SyncHandlerProtocol(Protocol):
    def handle(self, record: "LogRecordProtocol") -> None:
        ...

    def close(self) -> None:
        ...

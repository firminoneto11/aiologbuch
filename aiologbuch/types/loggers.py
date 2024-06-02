from typing import TYPE_CHECKING, Protocol, Self

if TYPE_CHECKING:
    from .types_ import FilterProtocol


class BaseLoggerProtocol(Protocol):
    def __call__(self, name: str, filter: "FilterProtocol") -> Self: ...


class AsyncLoggerProtocol(BaseLoggerProtocol):
    async def disable(self) -> None: ...


class SyncLoggerProtocol(BaseLoggerProtocol):
    def disable(self) -> None: ...
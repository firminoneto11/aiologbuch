from typing import TYPE_CHECKING, Protocol, Self

if TYPE_CHECKING:
    from .filters import FilterProtocol


class BaseLoggerProtocol(Protocol):
    def __call__(self, name: str, filter_: "FilterProtocol") -> Self: ...

    def _add_handler[T](self, handler: T) -> None: ...


class AsyncLoggerProtocol(BaseLoggerProtocol):
    async def _disable(self) -> None: ...


class SyncLoggerProtocol(BaseLoggerProtocol):
    def _disable(self) -> None: ...

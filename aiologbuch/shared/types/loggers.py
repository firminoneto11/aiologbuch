from typing import TYPE_CHECKING, Protocol, Self

if TYPE_CHECKING:
    from .filters import FilterProtocol
    from .general import LoggerMode


class BaseLoggerProtocol(Protocol):
    mode: "LoggerMode"

    def __call__(self, name: str, filter_: "FilterProtocol") -> Self: ...


class AsyncLoggerProtocol(BaseLoggerProtocol):
    async def _disable(self) -> None: ...


class SyncLoggerProtocol(BaseLoggerProtocol):
    def _disable(self) -> None: ...

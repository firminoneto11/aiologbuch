from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from logging import LogRecord

    from nlogging._types import AsyncHandlerProtocol, CallerInfo, LevelType, MessageType


class BaseAsyncLogger(ABC):
    @abstractmethod
    def __init__(self, name: str, level: "LevelType") -> None:
        ...

    @property
    @abstractmethod
    def level(self) -> int:
        ...

    @level.setter
    @abstractmethod
    def level(self, value: "LevelType") -> None:
        ...

    @property
    def _mem_addr(self) -> str:
        ...

    @abstractmethod
    async def debug(self, msg: "MessageType") -> None:
        ...

    @abstractmethod
    async def info(self, msg: "MessageType") -> None:
        ...

    @abstractmethod
    async def warning(self, msg: "MessageType") -> None:
        ...

    @abstractmethod
    async def error(
        self, msg: "MessageType", exc: Optional[BaseException] = None
    ) -> None:
        ...

    @abstractmethod
    async def critical(self, msg: "MessageType") -> None:
        ...

    @abstractmethod
    def _find_caller(self) -> "CallerInfo":
        ...

    @abstractmethod
    def _make_record(
        self,
        name: str,
        level: int,
        msg: "MessageType",
        filename: str,
        function_name: str,
        line_number: int,
        exc_info: Optional[BaseException] = None,
    ) -> "LogRecord":
        ...

    @abstractmethod
    async def _log(
        self, level: int, msg: "MessageType", exc_info: Optional[BaseException] = None
    ) -> None:
        ...

    @abstractmethod
    async def _handle(self, record: "LogRecord") -> None:
        ...

    @abstractmethod
    def _add_handler(self, handler: "AsyncHandlerProtocol") -> None:
        ...

    @abstractmethod
    def _remove_handler(self, handler: "AsyncHandlerProtocol") -> None:
        ...

    @abstractmethod
    def _has_handlers(self) -> bool:
        ...

    @abstractmethod
    async def _call_handlers(self, record: "LogRecord") -> None:
        ...

    @abstractmethod
    def _is_enabled_for(self, level: int) -> bool:
        ...

    @abstractmethod
    async def _disable(self) -> None:
        ...

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional, Self, TypedDict

if TYPE_CHECKING:
    from nlogging.handlers import BaseAsyncHandler
    from nlogging.records import LogRecord

    class CallerInfo(TypedDict):
        caller_filename: str
        caller_function_name: str
        caller_line_number: int

    type MessageType = str | dict


class BaseLogger(ABC):
    _handlers: dict[str, "BaseAsyncHandler"]

    @classmethod
    @abstractmethod
    def create_logger(cls, name: str, level: int | str) -> Self:
        raise NotImplementedError

    @abstractmethod
    def __init__(self, name: str, level: int | str) -> None:
        raise NotImplementedError

    @property
    @abstractmethod
    def level(self) -> int:
        raise NotImplementedError

    @level.setter
    @abstractmethod
    def level(self, value: int | str) -> None:
        raise NotImplementedError

    @property
    @abstractmethod
    def handlers(self) -> dict[str, "BaseAsyncHandler"]:
        raise NotImplementedError

    @abstractmethod
    async def debug(self, msg: "MessageType") -> None:
        raise NotImplementedError

    @abstractmethod
    async def info(self, msg: "MessageType") -> None:
        raise NotImplementedError

    @abstractmethod
    async def warning(self, msg: "MessageType") -> None:
        raise NotImplementedError

    @abstractmethod
    async def error(self, msg: "MessageType") -> None:
        raise NotImplementedError

    @abstractmethod
    async def exception(self, msg: "MessageType") -> None:
        raise NotImplementedError

    @abstractmethod
    async def critical(self, msg: "MessageType") -> None:
        raise NotImplementedError

    @abstractmethod
    def find_caller(self) -> "CallerInfo":
        raise NotImplementedError

    @abstractmethod
    def make_record(
        self,
        name: str,
        msg: "MessageType",
        level: int,
        filename: str,
        function_name: str,
        line_number: int,
        exc_info,
        extra: Optional[dict] = None,
    ) -> "LogRecord":
        raise NotImplementedError

    @abstractmethod
    async def _log(
        self,
        level: int,
        msg: "MessageType",
        exc_info: bool = False,
        extra: Optional[dict] = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def handle(self, record: "LogRecord") -> None:
        raise NotImplementedError

    @abstractmethod
    def add_handler(self, handler: "BaseAsyncHandler") -> None:
        raise NotImplementedError

    @abstractmethod
    def remove_handler(self, handler: "BaseAsyncHandler") -> None:
        raise NotImplementedError

    @abstractmethod
    def has_handlers(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def call_handlers(self, record: "LogRecord") -> None:
        raise NotImplementedError

    @abstractmethod
    def is_enabled_for(self, level: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def disable(self) -> None:
        raise NotImplementedError
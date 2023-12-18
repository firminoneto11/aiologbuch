from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Self, TypedDict

if TYPE_CHECKING:
    from nlogging.handlers import BaseAsyncHandler
    from nlogging.records import LogRecord

    class CallerInfo(TypedDict):
        caller_filename: str
        caller_function_name: str
        caller_line_number: int


class BaseLogger(ABC):
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

    @abstractmethod
    def setLevel(self, level: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def debug(self, msg: str | dict) -> None:
        raise NotImplementedError

    @abstractmethod
    async def info(self, msg: str | dict) -> None:
        raise NotImplementedError

    @abstractmethod
    async def warning(self, msg: str | dict) -> None:
        raise NotImplementedError

    @abstractmethod
    async def error(self, msg: str | dict) -> None:
        raise NotImplementedError

    @abstractmethod
    async def exception(self, msg: str | dict) -> None:
        raise NotImplementedError

    @abstractmethod
    async def critical(self, msg: str | dict) -> None:
        raise NotImplementedError

    @abstractmethod
    def findCaller(self, stack_info: bool = False, stacklevel: int = 1) -> "CallerInfo":
        raise NotImplementedError

    @abstractmethod
    def makeRecord(
        self,
        name: str,
        level: int,
        fn: str,
        lno: int,
        msg: str | dict,
        args: tuple,
        exc_info: bool,
        func=None,
        extra: dict | None = None,
        sinfo=None,
    ) -> "LogRecord":
        raise NotImplementedError

    @abstractmethod
    async def _log(
        self,
        level,
        msg,
        args,
        exc_info=None,
        extra=None,
        stack_info=False,
        stacklevel=1,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def handle(self, record: "LogRecord") -> None:
        raise NotImplementedError

    @abstractmethod
    def addHandler(self, handler: "BaseAsyncHandler") -> None:
        raise NotImplementedError

    @abstractmethod
    def removeHandler(self, handler: "BaseAsyncHandler") -> None:
        raise NotImplementedError

    @abstractmethod
    def hasHandlers(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def callHandlers(self, record: "LogRecord") -> None:
        raise NotImplementedError

    @abstractmethod
    def isEnabledFor(self, level: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def disable(self) -> None:
        raise NotImplementedError

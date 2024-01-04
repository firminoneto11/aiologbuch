from logging import LogRecord
from typing import Literal, Protocol, Self, TypedDict


class CallerInfo(TypedDict):
    caller_filename: str
    caller_function_name: str
    caller_line_number: int


class MapType(TypedDict):
    resource: "_ResourceProtocol"
    reference_count: int


class LoggerProtocol(Protocol):
    def __call__(self, name: str, level: "LevelType") -> Self:
        ...


class FormatterProtocol(Protocol):
    def format(self, record: LogRecord) -> bytes:
        ...


class _ResourceProtocol(Protocol):
    async def init_stream(self) -> None:
        ...

    async def send(self, msg: bytes) -> None:
        ...

    async def close(self) -> None:
        ...


class AsyncHandlerProtocol(Protocol):
    id: int
    filter: "FilterProtocol"

    async def close(self) -> None:
        ...

    async def handle(self, record: LogRecord) -> None:
        ...


class FilterProtocol(Protocol):
    def filter(self, record: LogRecord) -> bool:
        ...


type MessageType = str | dict
type LevelType = int | Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

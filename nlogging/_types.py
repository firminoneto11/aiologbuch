from types import TracebackType
from typing import Literal, TypedDict


class CallerInfo(TypedDict):
    caller_filename: str
    caller_function_name: str
    caller_line_number: int


type MessageType = str | dict
type LevelType = int | Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
type ExcInfo = tuple[type[BaseException], BaseException, TracebackType]
type OptExcInfo = ExcInfo | tuple[None, None, None]

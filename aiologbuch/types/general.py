from typing import Literal, TypedDict

type MessageType = str | dict
type LevelType = int | Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
type LoggerKind = Literal["async", "sync"]


class CallerInfo(TypedDict):
    caller_filename: str
    caller_function_name: str
    caller_line_number: int

from typing import Literal, TypedDict

type MessageType = str | dict
type LevelType = int | Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
type LoggerKind = Literal["async", "sync"]


class CallerInfo(TypedDict):
    filename: str
    function_name: str
    line_number: int

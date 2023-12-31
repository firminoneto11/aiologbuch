from typing import TypedDict


class CallerInfo(TypedDict):
    caller_filename: str
    caller_function_name: str
    caller_line_number: int


type MessageType = str | dict
type LevelType = int | str

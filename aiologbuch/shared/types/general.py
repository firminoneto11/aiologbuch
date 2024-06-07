from typing import Literal

type MessageType = str | dict
type LevelType = int | Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
type LoggerKind = Literal["async", "sync"]

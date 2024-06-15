from typing import Literal

type MessageType = str | dict
type LevelType = int | Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
type LoggerMode = Literal["async", "sync"]
type StreamBackendType = Literal["thread", "aiofile", "sync"]
type AsyncStreamBackendType = Literal["thread", "aiofile"]
type SyncStreamBackendType = Literal["sync"]

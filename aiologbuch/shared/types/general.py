from typing import Literal

type MessageType = str | dict
type LevelType = int | Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


type AsyncMode = Literal["async"]
type SyncMode = Literal["sync"]
type IOMode = AsyncMode | SyncMode


type StreamBackendType = Literal["thread", "aiofile", "sync"]
type AsyncStreamBackendType = Literal["thread", "aiofile"]
type SyncStreamBackendType = Literal["sync"]

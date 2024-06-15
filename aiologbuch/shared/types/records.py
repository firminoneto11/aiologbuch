from typing import TYPE_CHECKING, Optional, Protocol

if TYPE_CHECKING:
    from .general import MessageType


class LogRecordProtocol(Protocol):
    name: str
    levelno: int
    created: float
    msecs: float
    levelname: str
    process: Optional[int]
    processName: Optional[str]
    thread: Optional[int]
    threadName: Optional[str]
    pathname: str
    funcName: str
    lineno: int
    exc_text: Optional[str]
    msg: "MessageType"

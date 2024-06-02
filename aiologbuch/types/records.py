from typing import Optional, Protocol


class LogRecordProtocol(Protocol):
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

    def getMessage(self) -> str:
        ...

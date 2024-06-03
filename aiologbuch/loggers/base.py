from inspect import stack
from logging import LogRecord
from traceback import format_exception
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from aiologbuch.types import CallerInfo, LoggerKind, LogRecordProtocol, MessageType


class BaseLogger[HandlerProtocol]:
    _enabled = True
    _handlers: set[HandlerProtocol]
    kind: "LoggerKind"
    name: str

    def __init__(self, name: str):
        self.name = name
        self._handlers = set()

    def _find_caller(self) -> "CallerInfo":
        frame = stack()[3]  # 3 frames up from this one is the original caller
        return {
            "filename": frame.filename,
            "function_name": frame.function,
            "line_number": frame.lineno,
        }

    def _make_record(
        self,
        name: str,
        level: int,
        msg: "MessageType",
        filename: str,
        function_name: str,
        line_number: int,
        exc_info: Optional[BaseException] = None,
    ) -> "LogRecordProtocol":
        if exc_info:
            info = (type(exc_info), exc_info, exc_info.__traceback__)
            text = "".join(format_exception(exc_info, limit=None, chain=True))
        else:
            info, text = None, None

        record = LogRecord(
            name=name,
            level=level,
            pathname=filename,
            lineno=line_number,
            msg=msg,
            args=None,
            exc_info=info,
            func=function_name,
        )

        if text:
            record.exc_text = text

        return record

    def _add_handler(self, handler: HandlerProtocol):
        self._handlers.add(handler)

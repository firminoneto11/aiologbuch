from dataclasses import dataclass
from inspect import currentframe
from logging import LogRecord
from traceback import format_exception
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from aiologbuch.shared.types import FilterProtocol, IOMode, MessageType


@dataclass
class _StackFrame:
    filename: str
    function_name: str
    line_number: int


class BaseLogger[HandlerProtocol]:
    _enabled = True
    _handlers: set[HandlerProtocol]
    mode: "IOMode"
    name: str

    def __init__(self, name: str, filter_: "FilterProtocol"):
        self.name = name
        self._handlers = set()
        self._filter_object = filter_

    def _filter(self, level: int):
        return self._filter_object.filter(level=level)

    def _find_caller(self):
        # NOTE: The caller frame is located 3 frames up from the current one, which is
        # the one that calls 'debug', 'info', 'warning' and so on.
        caller_frame, CALLER_FRAME_LEVEL = currentframe(), 3
        try:
            for _ in range(CALLER_FRAME_LEVEL):
                caller_frame = caller_frame.f_back
            if caller_frame is None:
                raise ValueError()
        except (AttributeError, ValueError) as exc:
            raise RuntimeError("Could not find the caller's frame") from exc

        return _StackFrame(
            filename=caller_frame.f_code.co_filename,
            function_name=caller_frame.f_code.co_name,
            line_number=caller_frame.f_lineno,
        )

    def _make_record(
        self,
        name: str,
        level: int,
        msg: "MessageType",
        filename: str,
        function_name: str,
        line_number: int,
        exc_info: Optional[BaseException] = None,
    ):
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

from datetime import datetime, timezone
from time import strftime
from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from nlogging.records import LogRecord

    class CallerInfo(TypedDict):
        caller_filename: str
        caller_function_name: str
        caller_line_number: int


class BaseFormatter:
    # NOTE: The default datetime format follows ISO 8601
    DEFAULT_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"
    DEFAULT_MSEC_FORMAT = "%s.%03dZ"

    def converter(self, secs: float):
        return datetime.fromtimestamp(secs, tz=timezone.utc).timetuple()

    def format(self, record: "LogRecord") -> str:
        raise NotImplementedError("format() must be implemented in subclass")

    def format_time(self, record: "LogRecord"):
        timestamp = strftime(self.DEFAULT_DATE_FORMAT, self.converter(record.created))
        return self.DEFAULT_MSEC_FORMAT % (timestamp, record.msecs)

    def _ensure_str(self, log: str | bytes):
        if isinstance(log, str):
            return log
        if isinstance(log, bytes):
            return log.decode()

        raise TypeError(
            f"Serialized object must be of str or bytes type, not {type(log)}"
        )

    def _get_caller_info(self, record: "LogRecord") -> "CallerInfo":
        return {
            "caller_filename": (
                record.extra_data.get("caller_filename") or record.pathname
            ),
            "caller_function_name": (
                record.extra_data.get("caller_function_name") or record.funcName
            ),
            "caller_line_number": (
                record.extra_data.get("caller_line_number") or record.lineno
            ),
        }

from datetime import datetime, timezone
from time import strftime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aiologbuch.shared.types import LogRecordProtocol


class BaseFormatter:
    # NOTE: The default datetime format follows ISO 8601 using UTC time zone.
    DEFAULT_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"
    DEFAULT_MSEC_FORMAT = "%s.%03dZ"
    TERMINATOR = b"\n"

    def format(self, record: "LogRecordProtocol") -> bytes:
        raise NotImplementedError("format() must be implemented in subclasses")

    def _converter(self, secs: float):
        return datetime.fromtimestamp(secs, tz=timezone.utc).timetuple()

    def _format_time(self, record: "LogRecordProtocol"):
        timestamp = strftime(self.DEFAULT_DATE_FORMAT, self._converter(record.created))
        return self.DEFAULT_MSEC_FORMAT % (timestamp, record.msecs)

    def prepare_record(self, record: "LogRecordProtocol"):
        return {
            "timestamp": self._format_time(record),
            "level": record.levelname,
            "process_id": record.process,
            "process_name": record.processName,
            "thread_id": record.thread,
            "thread_name": record.threadName,
            "name": record.name,
            "filename": record.pathname,
            "function_name": record.funcName,
            "line_number": record.lineno,
            "traceback": record.exc_text,
            "message": record.msg,
        }

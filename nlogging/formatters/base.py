from datetime import datetime, timezone
from time import strftime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nlogging._types import LogRecordProtocol


class BaseFormatter:
    # NOTE: The default datetime format follows ISO 8601 using UTC time zone.
    DEFAULT_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"
    DEFAULT_MSEC_FORMAT = "%s.%03dZ"

    def converter(self, secs: float):
        return datetime.fromtimestamp(secs, tz=timezone.utc).timetuple()

    def format(self, record: "LogRecordProtocol") -> bytes:
        raise NotImplementedError("format() must be implemented in subclass")

    def format_time(self, record: "LogRecordProtocol"):
        timestamp = strftime(self.DEFAULT_DATE_FORMAT, self.converter(record.created))
        return self.DEFAULT_MSEC_FORMAT % (timestamp, record.msecs)

    def _ensure_bytes(self, log: str | bytes):
        if isinstance(log, bytes):
            return log
        if isinstance(log, str):
            return log.encode()

        raise TypeError(
            f"Serialized object must be of str or bytes type, not {type(log)}"
        )

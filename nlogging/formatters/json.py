import logging
import time
import typing
from datetime import datetime, timezone

# NOTE: orjson is optional
try:
    import orjson

    json = orjson
except ImportError:
    import json


class JsonFormatter(logging.Formatter):
    def converter(self, secs: float):
        return datetime.fromtimestamp(secs, tz=timezone.utc).timetuple()

    def format(self, record: logging.LogRecord):
        filename = record.__dict__.get("original_filename") or record.pathname
        functionName = record.__dict__.get("original_function_name") or record.funcName
        lineNumber = record.__dict__.get("original_line_number") or record.lineno

        log_data = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "filename": filename,
            "functionName": functionName,
            "lineNumber": lineNumber,
            "processId": record.process,
            "processName": record.processName,
            "threadId": record.thread,
            "threadName": record.threadName,
            "message": record.getMessage(),
        }

        log = json.dumps(log_data)

        if isinstance(log, str):
            return log
        if isinstance(log, bytes):
            return log.decode()

        raise TypeError(
            f"Serialized object must be of str or bytes type, not {type(log)}"
        )

    def formatTime(
        self, record: logging.LogRecord, datefmt: typing.Optional[str] = None
    ):
        if datefmt is None:
            raise ValueError("datefmt not specified")

        timestamp = time.strftime(datefmt, self.converter(record.created))

        if self.default_msec_format:
            timestamp = self.default_msec_format % (timestamp, record.msecs)

        return timestamp

from typing import TYPE_CHECKING

from .base import BaseFormatter

if TYPE_CHECKING:
    from logging._types import LogRecordProtocol


# NOTE: orjson is optional, but it's faster than stdlib json
try:
    import orjson as json
except ImportError:
    import json


class JsonFormatter(BaseFormatter):
    def format(self, record: "LogRecordProtocol"):
        log_data = {
            "timestamp": self.format_time(record),
            "level": record.levelname,
            "process_id": record.process,
            "process_name": record.processName,
            "thread_id": record.thread,
            "thread_name": record.threadName,
            "filename": record.pathname,
            "function_name": record.funcName,
            "line_number": record.lineno,
            "message": record.getMessage(),
        }

        if record.exc_text:
            log_data["exception"] = record.exc_text

        return self._ensure_bytes(log=json.dumps(log_data))

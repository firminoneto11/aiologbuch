from typing import TYPE_CHECKING

from .base import BaseFormatter

if TYPE_CHECKING:
    from logging import LogRecord


# NOTE: orjson is optional, but it's faster than json
try:
    import orjson as json
except ImportError:
    import json


class JsonFormatter(BaseFormatter):
    def format(self, record: "LogRecord"):
        caller_info = self._get_caller_info(record)

        log_data = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "filename": caller_info["caller_filename"],
            "functionName": caller_info["caller_function_name"],
            "lineNumber": caller_info["caller_line_number"],
            "processId": record.process,
            "processName": record.processName,
            "threadId": record.thread,
            "threadName": record.threadName,
            "message": record.getMessage(),
        }

        return self._ensure_str(log=json.dumps(log_data))

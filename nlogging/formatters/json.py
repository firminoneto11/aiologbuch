from typing import TYPE_CHECKING

from .base import BaseFormatter

if TYPE_CHECKING:
    from nlogging.records import LogRecord


# NOTE: orjson is optional, but it's faster than json
try:
    import orjson as json
except ImportError:
    import json


class JsonFormatter(BaseFormatter):
    def format(self, record: "LogRecord"):
        caller_info = self._get_caller_info(record)

        log_data = {
            "timestamp": self.format_time(record),
            "level": record.levelname,
            "process_id": record.process,
            "process_name": record.processName,
            "thread_id": record.thread,
            "thread_name": record.threadName,
            "filename": caller_info["caller_filename"],
            "function_name": caller_info["caller_function_name"],
            "line_number": caller_info["caller_line_number"],
            "message": record.getMessage(),
        }

        return self._ensure_str(log=json.dumps(log_data))

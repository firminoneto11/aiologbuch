import json
import re
from typing import TYPE_CHECKING

from .base import BaseFormatter

if TYPE_CHECKING:
    from aiologbuch.types import LogRecordProtocol


class JsonFormatter(BaseFormatter):
    def _ensure_safe(self, text: str):
        return re.sub(r"\\", r"\\\\", text)

    def format(self, record: "LogRecordProtocol"):
        data = {
            "timestamp": self.format_time(record),
            "level": record.levelname,
            "process_id": record.process,
            "process_name": record.processName,
            "thread_id": record.thread,
            "thread_name": record.threadName,
            "filename": record.pathname,
            "function_name": record.funcName,
            "line_number": record.lineno,
            "traceback": record.exc_text,
            "message": record.msg,
        }

        return self._ensure_safe(json.dumps(data)).encode()

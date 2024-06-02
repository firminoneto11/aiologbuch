from typing import TYPE_CHECKING

from .base import BaseFormatter

if TYPE_CHECKING:
    from aiologbuch._types import LogRecordProtocol


class LineFormatter(BaseFormatter):
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
            log_data["exception"] = "\n" + record.exc_text

        log = ""
        for idx, key in enumerate(log_data):
            log += f"[{key}] {log_data[key]}"
            if not idx == len(log_data) - 1:
                log += " | "

        return self._ensure_bytes(log=log)

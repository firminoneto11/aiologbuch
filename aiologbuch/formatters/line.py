from typing import TYPE_CHECKING

from .base import BaseFormatter

if TYPE_CHECKING:
    from aiologbuch.shared.types import LogRecordProtocol


class LineFormatter(BaseFormatter):
    def format(self, record: "LogRecordProtocol"):
        data = self.prepare_record(record=record)

        if record.exc_text:
            data["exception"] = record.exc_text

        log = ""
        for idx, key in enumerate(data):
            log += f"[{key}] {data[key]}"
            if not idx == len(data) - 1:
                log += " | "

        return log.encode() + self.TERMINATOR

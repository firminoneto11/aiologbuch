import json
import re
from typing import TYPE_CHECKING

from .base import BaseFormatter

if TYPE_CHECKING:
    from aiologbuch.shared.types import LogRecordProtocol


class JsonFormatter(BaseFormatter):
    def _ensure_safe(self, text: str):
        return re.sub(r"\\", r"\\\\", text)

    def format(self, record: "LogRecordProtocol"):
        data = self.prepare_record(record=record)
        return self._ensure_safe(json.dumps(data)).encode() + self.TERMINATOR

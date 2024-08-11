from typing import TYPE_CHECKING, Any

from .base import BaseFormatter

if TYPE_CHECKING:
    from aiologbuch.shared.types import LogRecordProtocol


class LineFormatter(BaseFormatter):
    def __init__(self, log_style: str | None = None):
        self._log_style = log_style

    @property
    def log_style(self):
        default = "{timestamp} | {level} | {name} | {message}"
        if not self._log_style:
            self._log_style = default
        return self._log_style

    def _parse(self, data: dict[str, Any]):
        log = self.log_style
        for key in data:
            placeholder = "{" + key + "}"
            log = log.replace(placeholder, str(data[key]))
        return log

    def format(self, record: "LogRecordProtocol"):
        data = self.prepare_record(record=record)
        log = self._parse(data=data)
        return log.encode() + self.TERMINATOR

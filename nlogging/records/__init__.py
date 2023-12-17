from logging import LogRecord as _LogRecord
from typing import Optional


class LogRecord(_LogRecord):
    def __init__(self, *args, extra_data: Optional[dict] = None, **kwargs):
        super().__init__(*args, **kwargs)
        if extra_data is None:
            extra_data = {}
        self._extra_data = extra_data

    @property
    def extra_data(self):
        return self._extra_data

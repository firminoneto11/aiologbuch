import logging
from typing import Optional


class LogRecord(logging.LogRecord):
    def __init__(self, *args, extra_data: Optional[dict] = None, **kwargs):
        super().__init__(*args, **kwargs)
        if extra_data is None:
            extra_data = {}
        self.extra_data = extra_data

    @property
    def extra_data(self):
        return self.extra_data

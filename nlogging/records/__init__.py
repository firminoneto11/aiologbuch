from logging import LogRecord as _LogRecord


class LogRecord(_LogRecord):
    def __init__(self, *args, **kwargs):
        self._extra_data = kwargs.pop("extra", {})
        super().__init__(*args, **kwargs)

    @property
    def extra_data(self):
        return self._extra_data

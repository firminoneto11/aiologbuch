from aiologbuch.types import BaseLoggerProtocol, FilterProtocol


class BaseLoggerManager[T: BaseLoggerProtocol]:
    _loggers: dict[str, T]
    _logger_class: T

    def __init__(self, logger_class: T):
        self._loggers = dict()
        self._logger_class = logger_class

    @property
    def loggers(self):
        return self._loggers

    @property
    def logger_class(self):
        return self._logger_class

    def get_logger(self, name: str, filter_: FilterProtocol):
        created = False
        if name not in self.loggers:
            self.loggers[name], created = self.logger_class(name, filter_), True

        return self.loggers[name], created

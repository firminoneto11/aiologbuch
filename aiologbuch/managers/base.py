from aiologbuch.types import BaseLoggerProtocol


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

    def get_logger[F](self, name: str, filter: F):
        created = False
        if name in self.loggers:
            return self.loggers[name], created

        self.loggers[name], created = (logger := self.logger_class(name, filter)), True

        return logger, created

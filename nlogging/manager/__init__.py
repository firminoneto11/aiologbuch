from typing import Optional, Self

from nlogging.loggers import BaseLogger
from nlogging.utils import is_direct_subclass


class LoggerManagerSingleton[LC: BaseLogger]:
    _instance: Optional[Self] = None
    _active_loggers: dict[str, LC]
    _logger_class: LC

    def __new__(cls, logger_class: LC):
        instance = cls._get_instance()
        instance._set_inner_logger(logger_class=logger_class)
        return instance

    @classmethod
    def _get_instance(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._active_loggers = {}
        return cls._instance

    def _set_inner_logger(self, logger_class: LC):
        if not is_direct_subclass(value=logger_class, base_cls=BaseLogger):
            raise TypeError(f"'logger_class' must be a {BaseLogger.__name__} subclass")
        self._logger_class = logger_class

    def get_logger(self, name: str, level: str | int):
        lc = self._logger_class

        if name not in self._active_loggers:
            self._active_loggers[name] = lc.create_logger(name=name, level=level)

        logger = self._active_loggers[name]

        if logger.level != level:
            logger.setLevel(level)

        return logger

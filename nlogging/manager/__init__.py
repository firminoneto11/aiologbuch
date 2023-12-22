from typing import Optional, Self

from nlogging.loggers import BaseLogger
from nlogging.utils import is_direct_subclass


class LoggerManagerSingleton[LC: BaseLogger]:
    _instance: Optional[Self] = None
    _active_loggers: dict[str, LC]
    _logger_class: LC

    def __new__(cls, logger_class: LC):
        self = cls._get_instance()
        self._set_inner_logger(logger_class=logger_class)
        return self

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

    def get_logger(self, name: str, level: int | str):
        if name not in self._active_loggers:
            self._active_loggers[name] = self._logger_class.create_logger(name, level)

        logger = self._active_loggers[name]

        if logger.level != level:
            logger.level = level

        return logger

    @classmethod
    async def clean_loggers(cls):
        self = cls._get_instance()
        for name in self._active_loggers:
            logger = self._active_loggers[name]
            await logger.disable()
        self._active_loggers = {}

    @classmethod
    async def disable_logger(cls, name: str):
        self = cls._get_instance()
        if (logger := self._active_loggers.pop(name, None)) is None:
            raise ValueError(f"{name!r} not in the map of active loggers")
        await logger.disable()

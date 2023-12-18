from typing import Optional, Self

from nlogging.loggers import BaseLogger


def _is_subclass[T: object](cls: type[T], base_cls: type[T]):
    subclasses = [el.__name__ for el in base_cls.__subclasses__()]
    return cls.__name__ in subclasses


class LoggerManagerSingleton[LC: BaseLogger]:
    _instance: Optional[Self] = None
    _active_loggers: dict[str, LC]
    _logger_class: LC

    def __new__(cls, logger_class: LC):
        if not cls._instance:
            cls._instance = super().__new__(cls)

        if not _is_subclass(cls=logger_class, base_cls=BaseLogger):
            raise TypeError(
                f"logger_class must be an instance of a {BaseLogger.__name__} subclass"
            )

        cls._instance._logger_class = logger_class

        return cls._instance

    def __init__(self, logger_class: LC):
        self._active_loggers = {}

    @property
    def active_loggers(self):
        return self._active_loggers

    def _create_logger(self, name: str, level: str | int):
        return self._logger_class.create_logger(name=name, level=level)

    def get_logger(self, name: str, level: str | int):
        if name not in self.active_loggers:
            self.active_loggers[name] = self._create_logger(name=name, level=level)

        logger = self.active_loggers[name]

        if logger.level != level:
            logger.setLevel(level)

        return logger

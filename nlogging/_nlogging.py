from typing import Literal

from .loggers import NLogger
from .manager import LoggerManagerSingleton
from .settings import ROOT_LOGGER_NAME


def get_logger(
    name: str = ROOT_LOGGER_NAME,
    level: int | Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO",
):
    """
    This function is used to get a logger instance. If you inform the same name, it
    will always return the same logger.

    :param name: The name of the logger. Default is nlogger, which is the root logger.
    :param level: The level of the logger. Default is INFO.

    :return: A NLogger instance.
    """
    manager = LoggerManagerSingleton[NLogger](logger_class=NLogger)
    return manager.get_logger(name=name, level=level)

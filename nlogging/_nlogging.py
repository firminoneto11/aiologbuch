from typing import Literal

from .loggers import NLogger
from .manager import LoggerManagerSingleton
from .settings import ROOT_LOGGER_NAME


def get_logger(
    name: str = ROOT_LOGGER_NAME,
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO",
):
    """
    This function is used to get a logger instance.

    :param name: The name of the logger. Default is nlogger, which is the root.
    :param level: The level of the logger. Default is INFO.
    """
    manager = LoggerManagerSingleton[NLogger](logger_class=NLogger)
    return manager.get_logger(name=name, level=level)

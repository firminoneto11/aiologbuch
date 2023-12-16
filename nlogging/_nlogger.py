import asyncio
import inspect
import logging
import sys
import typing
from functools import lru_cache, wraps
from os import getenv

from .formatters import JsonFormatter


def wrapped_cache[**Spec, ReturnType](func: typing.Callable[Spec, ReturnType]):
    @wraps(func)
    def wrapper(*args: Spec.args, **kwargs: Spec.kwargs) -> ReturnType:
        return lru_cache(maxsize=None, typed=True)(func)(*args, **kwargs)

    return wrapper


@wrapped_cache
def get_logger(
    name: str,
    level: typing.Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO",
):
    """
    This function is used to get a logger instance.

    :param name: The name of the logger.
    :param level: The level of the logger. Default is INFO.
    """
    level_ = {
        "INFO": logging.INFO,
        "DEBUG": logging.DEBUG,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }
    return NLogger(name=name, level=level_[level])


class NLogger:
    _logger: logging.Logger

    def __init__(self, name: str, level: int = logging.INFO):
        fmt = self._get_formatter()

        stderr_handler = logging.StreamHandler(sys.stderr)
        stderr_handler.setLevel(level=level)
        stderr_handler.setFormatter(fmt=fmt)

        # TODO: Fix wrapped_cache function: It's not caching
        # TODO: Check if the logger is already created before setting stuff again,
        # meaning, make this function idempotent
        # logging.Logger.manager.getLogger

        self._logger = logging.getLogger(name=name)
        self._logger.setLevel(level=level)
        self._logger.addHandler(stderr_handler)

    def _get_formatter(self):
        # NOTE: The default datetime format is ISO 8601
        DEFAULT_DATE_FORMAT = getenv("NLOGGING_DATE_FORMAT", "%Y-%m-%dT%H:%M:%S")
        DEFAULT_MSEC_FORMAT = getenv("NLOGGING_MSEC_FORMAT", "%s.%03dZ")

        formatter = JsonFormatter(datefmt=DEFAULT_DATE_FORMAT)
        formatter.default_msec_format = DEFAULT_MSEC_FORMAT

        return formatter

    def _get_previous_stack_data(self):
        previous_stack = inspect.stack()[2]
        return {
            "original_filename": previous_stack.filename,
            "original_function_name": previous_stack.function,
            "original_line_number": previous_stack.lineno,
        }

    # Sync Logging
    def debug(self, message: str | dict):
        self._logger.debug(message, stacklevel=2)

    def info(self, message: str | dict):
        self._logger.debug(message, stacklevel=2)

    def warning(self, message: str | dict):
        self._logger.debug(message, stacklevel=2)

    def error(self, message: str | dict):
        self._logger.debug(message, stacklevel=2)

    def critical(self, message: str | dict):
        self._logger.debug(message, stacklevel=2)

    # Async Logging
    async def aDebug(self, message: str | dict):
        await asyncio.to_thread(
            self._logger.debug, message, extra=self._get_previous_stack_data()
        )

    async def aInfo(self, message: str | dict):
        await asyncio.to_thread(
            self._logger.info, message, extra=self._get_previous_stack_data()
        )

    async def aWarning(self, message: str | dict):
        await asyncio.to_thread(
            self._logger.warning, message, extra=self._get_previous_stack_data()
        )

    async def aError(self, message: str | dict):
        await asyncio.to_thread(
            self._logger.error, message, extra=self._get_previous_stack_data()
        )

    async def aCritical(self, message: str | dict):
        await asyncio.to_thread(
            self._logger.critical, message, extra=self._get_previous_stack_data()
        )

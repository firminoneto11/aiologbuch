import asyncio
import inspect
import json
import logging
import sys
import time
import typing
from datetime import datetime, timezone
from functools import lru_cache
from os import getenv


@lru_cache(maxsize=None, typed=True)
def get_logger(
    name: str,
    level: typing.Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO",
):
    level_ = {
        "INFO": logging.INFO,
        "DEBUG": logging.DEBUG,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }
    return NLogger(name=name, level=level_[level])


class LogFilter:
    _level: int

    def __init__(self, level: int):
        self._level = level

    @property
    def level(self):
        return self._level

    def filter(self, record: logging.LogRecord):
        return self.level == record.levelno


class JsonFormatter(logging.Formatter):
    def converter(self, secs: float):
        return datetime.fromtimestamp(secs, tz=timezone.utc).timetuple()

    def format(self, record: logging.LogRecord):
        filename = record.__dict__.get("original_filename") or record.pathname
        functionName = record.__dict__.get("original_function_name") or record.funcName
        lineNumber = record.__dict__.get("original_line_number") or record.lineno

        log_data = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "filename": filename,
            "functionName": functionName,
            "lineNumber": lineNumber,
            "processId": record.process,
            "processName": record.processName,
            "threadId": record.thread,
            "threadName": record.threadName,
            "message": record.getMessage(),
        }

        return json.dumps(log_data)

    def formatTime(
        self, record: logging.LogRecord, datefmt: typing.Optional[str] = None
    ):
        if datefmt is None:
            raise ValueError("datefmt not specified")

        timestamp = time.strftime(datefmt, self.converter(record.created))

        if self.default_msec_format:
            timestamp = self.default_msec_format % (timestamp, record.msecs)

        return timestamp


class NLogger:
    _logger: logging.Logger

    def __init__(self, name: str, level: int = logging.INFO):
        fmt = self._get_formatter()

        # TODO: Add support for file logging
        # TODO: Add support for log rotation
        # TODO: Add support for multiple file loggers

        # for handler in handlers:
        #     if handler.log_only_one_level:  # pragma: no cover
        #         handler.file_handler.addFilter(filter=LogFilter(level=handler.level))

        #     handler.file_handler.setLevel(level=handler.level)
        #     handler.file_handler.setFormatter(fmt=fmt)
        #     self._logger.addHandler(handler.file_handler)

        stderr_handler = logging.StreamHandler(sys.stderr)
        stderr_handler.setLevel(level=level)
        stderr_handler.setFormatter(fmt=fmt)

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

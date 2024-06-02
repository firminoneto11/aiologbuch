from functools import lru_cache

from aiologbuch.types import BaseLoggerProtocol

from .async_ import AsyncLoggerManager as _AsyncManager
from .sync import SyncLoggerManager as _SyncManager


@lru_cache(maxsize=2, typed=True)
def get_logger_manager[T: BaseLoggerProtocol](logger_class: T):
    if logger_class.kind == "async":
        return _AsyncManager(logger_class)
    return _SyncManager(logger_class)

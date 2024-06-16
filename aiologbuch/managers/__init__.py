from functools import lru_cache as _lru_cache

from aiologbuch.shared.enums import IOModeEnum
from aiologbuch.shared.types import BaseLoggerProtocol as _BaseLoggerProtocol

from .async_ import AsyncLoggerManager as _AsyncManager
from .sync import SyncLoggerManager as _SyncManager


@_lru_cache(maxsize=2, typed=True)
def get_logger_manager[T: _BaseLoggerProtocol](logger_class: T):
    if logger_class.mode == IOModeEnum.ASYNC:
        return _AsyncManager(logger_class)
    return _SyncManager(logger_class)

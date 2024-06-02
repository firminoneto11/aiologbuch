from functools import lru_cache

from aiologbuch.types import AsyncLoggerProtocol, SyncLoggerProtocol

from .async_ import AsyncLoggerManager
from .sync import SyncLoggerManager


@lru_cache(maxsize=1, typed=True)
def get_async_manager[T: AsyncLoggerProtocol](logger_class: T):
    return AsyncLoggerManager(logger_class)


@lru_cache(maxsize=1, typed=True)
def get_sync_manager[T: SyncLoggerProtocol](logger_class: T):
    return SyncLoggerManager(logger_class)

from typing import overload

from aiologbuch.shared.enums import IOModeEnum
from aiologbuch.shared.types import AsyncMode, BaseLoggerProtocol, IOMode, SyncMode

from .async_ import AsyncLoggerManager as AsyncManager
from .sync import SyncLoggerManager as SyncManager


@overload
def get_logger_manager(
    mode: AsyncMode, logger_class: BaseLoggerProtocol
) -> AsyncManager: ...


@overload
def get_logger_manager(
    mode: SyncMode, logger_class: BaseLoggerProtocol
) -> SyncManager: ...


def get_logger_manager(mode: IOMode, logger_class: BaseLoggerProtocol):
    if mode == IOModeEnum.ASYNC:
        return AsyncManager(logger_class)
    return SyncManager(logger_class)

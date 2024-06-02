from aiologbuch.types import SyncLoggerProtocol

from .base import BaseLoggerManager


class SyncLoggerManager(BaseLoggerManager[SyncLoggerProtocol]):
    def disable(self):
        [self.loggers[name].disable() for name in self.loggers]

    def disable_logger(self, name: str):
        if logger := self.loggers.pop(name, None):
            logger.disable()

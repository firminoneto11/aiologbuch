from aiologbuch.types import AsyncLoggerProtocol

from .base import BaseLoggerManager


class AsyncLoggerManager(BaseLoggerManager[AsyncLoggerProtocol]):
    async def disable(self):
        [await self.loggers[name].disable() for name in self.loggers]

    async def disable_logger(self, name: str):
        if logger := self.loggers.pop(name, None):
            await logger.disable()

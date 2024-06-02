import atexit

from asyncer import syncify

from .manager import resource_manager


class AsyncStreamMixin:
    @property
    def manager(self):
        return resource_manager

    async def write_and_flush(self, msg: bytes):
        await self.manager.asend_message(msg)

    async def close(self):
        func = syncify(self.manager.aclose)
        atexit.register(func)

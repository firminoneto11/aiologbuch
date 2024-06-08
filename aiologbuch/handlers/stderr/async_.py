import atexit

from aiologbuch.shared.utils import syncify

from .manager import resource_manager


class AsyncStderrMixin:
    @property
    def manager(self):
        return resource_manager

    async def write_and_flush(self, msg: bytes):
        await self.manager.asend_message(msg)

    async def close(self):
        atexit.register(syncify(self.manager.aclose))

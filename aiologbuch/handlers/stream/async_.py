import atexit
from typing import TYPE_CHECKING

from asyncer import syncify

from .manager import resource_manager

if TYPE_CHECKING:
    from aiologbuch.types import FilterProtocol, FormatterProtocol


class AsyncStreamMixin:
    def __init__(self, filter: "FilterProtocol", formatter: "FormatterProtocol"):
        super().__init__(filter=filter, formatter=formatter)

    @property
    def manager(self):
        return resource_manager

    async def write_and_flush(self, msg: bytes):
        await self.manager.asend_message(msg)

    async def close(self):
        func = syncify(self.manager.aclose)
        atexit.register(func)

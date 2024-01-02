from asyncio import sleep
from asyncio.protocols import Protocol
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from asyncio import StreamWriter


class AIOProtocol(Protocol):
    async def _drain_helper(self):
        ...

    async def _get_close_waiter(self, transport: "StreamWriter"):
        while transport.transport._pipe is not None:
            await sleep(0)  # Skips one event loop iteration

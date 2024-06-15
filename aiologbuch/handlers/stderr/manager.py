import sys
from asyncio import StreamWriter, get_running_loop, sleep
from asyncio.protocols import Protocol
from dataclasses import dataclass
from typing import Optional, TextIO

from aiologbuch.shared.conf import GLOBAL_STDERR_LOCK
from aiologbuch.shared.utils import async_lock_context, sync_lock_context


class _AIOProto(Protocol):
    async def _drain_helper(self): ...

    async def _get_close_waiter(self, transport: StreamWriter):
        while transport.transport._pipe is not None:
            await sleep(0)  # NOTE: Skips one event loop iteration


@dataclass
class _ResourceManager:
    stream: TextIO
    _writer: Optional[StreamWriter] = None
    _closed = False

    @property
    def closed(self):
        return self._closed

    async def asend_message(self, msg: bytes):
        async with async_lock_context(lock=GLOBAL_STDERR_LOCK):
            if self.closed:
                raise RuntimeError("Writer was closed")

            if not self._writer:
                loop = get_running_loop()
                transport, protocol = await loop.connect_write_pipe(
                    _AIOProto, self.stream
                )
                self._writer = StreamWriter(
                    transport=transport, protocol=protocol, reader=None, loop=loop
                )

            self._writer.write(msg)
            await self._writer.drain()

    def send_message(self, msg: bytes):
        with sync_lock_context(lock=GLOBAL_STDERR_LOCK):
            if self.closed:
                raise RuntimeError("Writer was closed")
            self.stream.write(msg.decode())
            self.stream.flush()

    async def aclose(self):
        async with async_lock_context(lock=GLOBAL_STDERR_LOCK):
            if (self.closed) or (not self._writer):
                return

            self._writer.write(b"Closing stderr...")
            await self._writer.drain()

            self._writer.close()
            await self._writer.wait_closed()
            self._writer, self._closed = None, True

    def close(self):
        with sync_lock_context(lock=GLOBAL_STDERR_LOCK):
            if self.closed:
                return
            self.stream.write("Closing stderr...")
            self.stream.flush()
            self.stream.close()
            self._closed = True


resource_manager = _ResourceManager(stream=sys.stderr)

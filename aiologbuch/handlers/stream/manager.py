import sys
from asyncio import StreamWriter, get_running_loop, sleep
from asyncio.protocols import Protocol
from dataclasses import dataclass
from typing import Optional, TextIO

from asyncer import syncify

from aiologbuch.shared import STDERR_LOCK


class _AIOProto(Protocol):
    async def _drain_helper(self):
        ...

    async def _get_close_waiter(self, transport: StreamWriter):
        while transport.transport._pipe is not None:
            await sleep(0)  # Skips one event loop iteration


@dataclass
class _ResourceManager:
    stream: TextIO
    _writer: Optional[StreamWriter] = None
    _closed = False

    @property
    def closed(self):
        return self._closed

    async def asend_message(self, msg: bytes):
        async with STDERR_LOCK:
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
        syncify(STDERR_LOCK.acquire)()
        try:
            self.stream.write(msg)
            self.stream.flush()
        finally:
            syncify(STDERR_LOCK.release)()

    # NOTE: Is it wise to close the sys.stderr?

    async def aclose(self):
        async with STDERR_LOCK:
            if (self.closed) or (not self._writer):
                return

            self._writer.write(b"Closing stderr...")
            await self._writer.drain()

            self._writer.close()
            await self._writer.wait_closed()
            self._writer, self._closed = None, True

    def close(self):
        syncify(STDERR_LOCK.acquire)()
        try:
            self.stream.write("Closing stderr...")
            self.stream.flush()
            self.stream.close()
        finally:
            syncify(STDERR_LOCK.release)()


resource_manager = _ResourceManager(stream=sys.stderr)

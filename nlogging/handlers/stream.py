from asyncio import StreamWriter, get_running_loop
from sys import stderr
from typing import TYPE_CHECKING, Optional

from anyio import Lock

from nlogging.protocols import AIOProtocol

if TYPE_CHECKING:
    from logging import LogRecord

    from nlogging._types import LevelType
    from nlogging.formatters import BaseFormatter

from .base import BaseAsyncHandler, BaseSyncHandler

_stderr_writer = None
_stderr_lock = Lock()
_closed = False


async def _get_stderr_writer():
    global _stderr_writer
    global _stderr_lock
    global _closed

    if _closed:
        raise RuntimeError("Writer was closed")

    if _stderr_writer:
        return _stderr_writer

    loop = get_running_loop()

    async with _stderr_lock:
        transport, protocol = await loop.connect_write_pipe(AIOProtocol, stderr)
        _stderr_writer = StreamWriter(
            transport=transport, protocol=protocol, reader=None, loop=loop
        )

    return _stderr_writer


async def _close_stderr_writer():
    global _stderr_writer
    global _stderr_lock
    global _closed

    if (_closed) or (not _stderr_writer):
        return

    async with _stderr_lock:
        await _stderr_writer.drain()
        _stderr_writer.close()
        await _stderr_writer.wait_closed()
        _stderr_writer = None
        _closed = True


class AsyncStreamHandler(BaseAsyncHandler):
    _writer: Optional[StreamWriter]

    terminator = b"\n"

    @property
    def lock(self):
        global _stderr_lock
        return _stderr_lock

    def __init__(self, level: "LevelType", formatter: "BaseFormatter"):
        super().__init__(level=level, formatter=formatter)

    async def emit(self, record: "LogRecord"):
        try:
            msg = self.format(record) + self.terminator
            await self.write_and_flush(msg)
        except:  # noqa
            await self.handle_error(record)

    async def write_and_flush(self, msg: bytes):
        writer = await _get_stderr_writer()
        async with self.lock:
            writer.write(msg)
            await writer.drain()

    async def close(self):
        pass


class SyncStreamHandler(BaseSyncHandler):
    terminator = b"\n"

    def __init__(self, level: "LevelType", formatter: "BaseFormatter"):
        super().__init__(level=level, formatter=formatter)

    def emit(self, record: "LogRecord"):
        try:
            msg = self.format(record) + self.terminator
            self.write_and_flush(msg)
        except:  # noqa
            self.handle_error(record)

    def write_and_flush(self, msg: bytes):
        with self.lock:
            stderr.write(msg.decode())
            stderr.flush()

    def close(self):
        pass

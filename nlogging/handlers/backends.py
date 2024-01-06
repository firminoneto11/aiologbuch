from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

from aiofile import async_open
from anyio.streams.file import FileWriteStream

if TYPE_CHECKING:
    from aiofile import BinaryFileWrapper

    from nlogging._types import BackendProtocol


def get_backend(name: Literal["thread", "aiofile"]) -> "BackendProtocol":
    match name.lower().strip():
        case "thread":
            return ThreadBackend
        case "aiofile":
            return AIOBackend
        case _:
            raise ValueError("Invalid backend name")


@dataclass
class AIOBackend:
    filename: str
    _file_stream: "BinaryFileWrapper | None" = None

    async def init(self):
        if not self._file_stream:
            self._file_stream = await async_open(self.filename, mode="a+b")

    async def send(self, msg: bytes):
        if not self._file_stream:
            raise RuntimeError("Stream is not initialized")
        await self._file_stream.write(msg)

    async def close(self):
        if self._file_stream:
            await self._file_stream.close()
            self._file_stream = None


@dataclass
class ThreadBackend:
    filename: str
    _file_stream: "FileWriteStream | None" = None

    async def init(self):
        if not self._file_stream:
            self._file_stream = await FileWriteStream.from_path(self.filename, True)

    async def send(self, msg: bytes):
        if not self._file_stream:
            raise RuntimeError("Stream is not initialized")
        await self._file_stream.send(msg)

    async def close(self):
        if self._file_stream:
            await self._file_stream.aclose()
            self._file_stream = None

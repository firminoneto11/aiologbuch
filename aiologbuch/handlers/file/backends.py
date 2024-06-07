from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal, Optional

from anyio.streams.file import FileWriteStream

try:
    from aiofile import async_open as aopen
except ImportError:
    aopen = None


if TYPE_CHECKING:
    from aiologbuch.shared.types import BinaryFileWrapperProtocol, StreamProtocol


def get_stream_backend(name: Literal["thread", "aiofile"]) -> "StreamProtocol":
    backends = {
        "thread": _ThreadBackend,
        "aiofile": _AIOFileBackend,
    }

    if backend := backends.get(name):
        return backend

    raise ValueError(f"Unsupported stream backend: {name!r}")


@dataclass
class _ThreadBackend:
    filename: str
    stream: Optional[FileWriteStream] = None

    async def open(self):
        if not self.stream:
            self.stream = await FileWriteStream.from_path(self.filename, True)

    async def send(self, msg: bytes):
        if not self.stream:
            raise RuntimeError(f"{self.filename!r}'s stream was not initialized")
        await self.stream.send(msg)

    async def close(self):
        if self.stream:
            await self.stream.aclose()
            self.stream = None


@dataclass
class _AIOFileBackend:
    filename: str
    stream: Optional["BinaryFileWrapperProtocol"] = None

    async def open(self):
        if aopen is None:
            raise RuntimeError("'aiofile' is not installed")

        if not self.stream:
            self.stream = await aopen(self.filename, mode="a+b")

    async def send(self, msg: bytes):
        if not self.stream:
            raise RuntimeError(f"{self.filename!r}'s stream was not initialized")
        await self.stream.write(msg)

    async def close(self):
        if self.stream:
            await self.stream.close()
            self.stream = None

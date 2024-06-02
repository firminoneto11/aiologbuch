from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal, Optional

from anyio.streams.file import FileWriteStream

# NOTE: aiofile is optional but is recommended for native async file writing
try:
    from aiofile import async_open as aopen
except ImportError:
    aopen = None

if TYPE_CHECKING:
    from aiologbuch.types import BackendProtocol, BinaryFileWrapperProtocol


def get_backend(name: Literal["thread", "aiofile"]) -> "BackendProtocol":
    backends = {"thread": ThreadBackend, "aiofile": AIOFileBackend}

    backend_name = name.lower().strip()
    if (backend := backends.get(backend_name)) is None:
        raise ValueError(f"Unknown file backend: {backend_name}")

    if aopen is None:
        return ThreadBackend

    return backend


@dataclass
class AIOFileBackend:
    filename: str
    _file_stream: "Optional[BinaryFileWrapperProtocol]" = None

    async def init(self):
        if aopen is None:
            raise RuntimeError("'aiofile' is not installed")

        if not self._file_stream:
            self._file_stream = await aopen(self.filename, mode="a+b")

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
    _file_stream: "Optional[FileWriteStream]" = None

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

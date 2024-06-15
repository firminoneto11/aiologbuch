from dataclasses import dataclass
from io import TextIOWrapper
from typing import TYPE_CHECKING, Optional, Union, cast, overload

from anyio.streams.file import FileWriteStream

try:
    from aiofile import async_open as aopen
except ImportError:
    aopen = None


if TYPE_CHECKING:
    from aiologbuch.shared.types import (
        AsyncStreamBackendType,
        AsyncStreamProtocol,
        BinaryFileWrapperProtocol,
        StreamBackendType,
        SyncStreamBackendType,
        SyncStreamProtocol,
    )

    @overload
    def get_stream_backend(
        name: "AsyncStreamBackendType",
    ) -> "AsyncStreamProtocol": ...

    @overload
    def get_stream_backend(name: "SyncStreamBackendType") -> "SyncStreamProtocol": ...


def get_stream_backend(name: "StreamBackendType"):
    backends = {
        "thread": _ThreadBackend,
        "aiofile": _AIOFileBackend,
        "sync": _SyncFileBackend,
    }

    if backend := backends.get(name):
        return cast(Union["AsyncStreamProtocol", "SyncStreamProtocol"], backend)

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


@dataclass
class _SyncFileBackend:
    filename: str
    stream: Optional[TextIOWrapper] = None

    def open(self):
        if not self.stream:
            self.stream = open(file=self.filename, mode="ab", encoding="utf-8")

    def send(self, msg: bytes):
        if not self.stream:
            raise RuntimeError(f"{self.filename!r}'s stream was not initialized")
        self.stream.write(msg)

    def close(self):
        if self.stream:
            self.stream.close()
            self.stream = None

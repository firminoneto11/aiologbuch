from asyncio import Lock
from typing import TYPE_CHECKING, Union

from aiologbuch.shared.conf import STREAM_BACKEND
from aiologbuch.shared.utils import sync_lock_context

from .backends import get_stream_backend

if TYPE_CHECKING:
    from aiologbuch.shared.types import AsyncStreamProtocol, SyncStreamProtocol


class _ResourceManager:
    _lock: Lock
    _resources: dict[str, "_StreamResource"]

    def __init__(self):
        self._lock = Lock()
        self._resources = dict()

    @property
    def resources(self):
        return self._resources

    @property
    def lock(self):
        return self._lock

    async def aopen_stream(self, filename: str):  # type: ignore [no-untyped-def]
        async with self.lock:
            if (resource := self.resources.get(filename)) is None:
                resource = _StreamResource(filename=filename)
                self.resources[filename] = resource
            resource.reference_count += 1

        await resource.aopen()

    def open_stream(self, filename: str):  # type: ignore [no-untyped-def]
        with sync_lock_context(lock=self.lock):
            if (resource := self.resources.get(filename)) is None:
                resource = _StreamResource(filename=filename, kind="sync")
                self.resources[filename] = resource
            resource.reference_count += 1

        resource.open()

    async def asend_message(self, filename: str, msg: bytes):  # type: ignore [no-untyped-def]
        async with self.lock:
            if (resource := self.resources.get(filename)) is None:
                raise RuntimeError(f"{filename!r}'s stream was not initialized")

        await resource.asend(msg=msg)

    def send_message(self, filename: str, msg: bytes):  # type: ignore [no-untyped-def]
        with sync_lock_context(lock=self.lock):
            if (resource := self.resources.get(filename)) is None:
                raise RuntimeError(f"{filename!r}'s stream was not initialized")

        resource.send(msg=msg)

    async def aclose_stream(self, filename: str):  # type: ignore [no-untyped-def]
        stream = None

        async with self.lock:
            if resource := self.resources.get(filename):
                resource.reference_count -= 1
                if resource.reference_count <= 0:
                    stream = self.resources.pop(filename)

        if stream:
            await stream.aclose()

    def close_stream(self, filename: str):  # type: ignore [no-untyped-def]
        stream = None

        with sync_lock_context(lock=self.lock):
            if resource := self.resources.get(filename):
                resource.reference_count -= 1
                if resource.reference_count <= 0:
                    stream = self.resources.pop(filename)

        if stream:
            stream.close()


class _StreamResource:
    _lock: Lock
    _filename: str
    _stream: Union["AsyncStreamProtocol", "SyncStreamProtocol"]
    reference_count: int

    def __init__(self, filename: str, kind: str = "async"):
        self._lock = Lock()
        self._filename = filename
        self._stream = _AsyncStream(filename=self.filename)
        self.reference_count = 0

    @property
    def lock(self):
        return self._lock

    @property
    def filename(self):
        return self._filename

    @property
    def stream(self):
        return self._stream

    async def aopen(self):
        async with self.lock:
            await self.stream.open()

    def open(self):
        ...

    async def asend(self, msg: bytes):  # type: ignore [no-untyped-def]
        async with self.lock:
            await self.stream.send(msg)

    def send(self, msg: bytes):  # type: ignore [no-untyped-def]
        ...

    async def aclose(self):
        async with self.lock:
            await self.stream.close()

    def close(self):
        ...


_AsyncStream = get_stream_backend("thread")

_SyncStream = get_stream_backend("sync")

resource_manager = _ResourceManager()

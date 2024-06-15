from asyncio import Lock
from threading import Lock as ThreadLock
from typing import TYPE_CHECKING, Literal, Union

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

    def ensure_correct_mode(
        self, resource: "_StreamResource", mode: Literal["async", "sync"]
    ):
        if resource.mode != mode:
            raise

    async def aopen_stream(self, filename: str):
        async with self.lock:
            if (resource := self.resources.get(filename)) is None:
                resource = _StreamResource(filename=filename, mode="async")
                self.resources[filename] = resource

            self.ensure_correct_mode(resource=resource, mode="async")

            resource.reference_count += 1

        await resource.aopen()

    def open_stream(self, filename: str):
        with sync_lock_context(lock=self.lock):
            if (resource := self.resources.get(filename)) is None:
                resource = _StreamResource(filename=filename, mode="sync")
                self.resources[filename] = resource

            self.ensure_correct_mode(resource=resource, mode="sync")

            resource.reference_count += 1

        resource.open()

    async def asend_message(self, filename: str, msg: bytes):
        async with self.lock:
            if (resource := self.resources.get(filename)) is None:
                raise RuntimeError(f"{filename!r}'s stream was not initialized")

            self.ensure_correct_mode(resource=resource, mode="async")

        await resource.asend(msg=msg)

    def send_message(self, filename: str, msg: bytes):
        with sync_lock_context(lock=self.lock):
            if (resource := self.resources.get(filename)) is None:
                raise RuntimeError(f"{filename!r}'s stream was not initialized")

            self.ensure_correct_mode(resource=resource, mode="sync")

        resource.send(msg=msg)

    async def aclose_stream(self, filename: str):
        stream = None

        async with self.lock:
            if (resource := self.resources.get(filename)) is None:
                return

            self.ensure_correct_mode(resource=resource, mode="async")

            resource.reference_count -= 1
            if resource.reference_count <= 0:
                stream = self.resources.pop(filename)

        if stream:
            await stream.aclose()

    def close_stream(self, filename: str):
        stream = None

        with sync_lock_context(lock=self.lock):
            if (resource := self.resources.get(filename)) is None:
                return

            self.ensure_correct_mode(resource=resource, mode="sync")

            resource.reference_count -= 1
            if resource.reference_count <= 0:
                stream = self.resources.pop(filename)

        if stream:
            stream.close()


class _StreamResource:
    _filename: str
    _lock: Lock | ThreadLock
    _stream: Union["AsyncStreamProtocol", "SyncStreamProtocol"]

    reference_count: int
    mode: Literal["async", "sync"]

    def __init__(self, filename: str, mode: Literal["async", "sync"]):
        self._filename = filename

        if mode == "async":
            self._lock = Lock()
            self._stream = _AsyncStream(filename=self.filename)
        else:
            self._lock = ThreadLock()
            self._stream = _SyncStream(filename=self.filename)

        self.reference_count = 0
        self.mode = mode

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
        if self.mode != "async":
            raise

        async with self.lock:
            await self.stream.open()

    def open(self):
        if self.mode != "sync":
            raise

        with self.lock:
            self.stream.open()

    async def asend(self, msg: bytes):
        if self.mode != "async":
            raise

        async with self.lock:
            await self.stream.send(msg)

    def send(self, msg: bytes):
        if self.mode != "sync":
            raise

        with self.lock:
            self.stream.send(msg)

    async def aclose(self):
        if self.mode != "async":
            raise

        async with self.lock:
            await self.stream.close()

    def close(self):
        if self.mode != "sync":
            raise

        with self.lock:
            self.stream.close()


_AsyncStream = get_stream_backend(STREAM_BACKEND)

_SyncStream = get_stream_backend("sync")

resource_manager = _ResourceManager()

from asyncio import Lock
from threading import Lock as ThreadLock
from typing import TYPE_CHECKING, Union, cast

from aiologbuch.shared.conf import settings
from aiologbuch.shared.enums import IOModeEnum
from aiologbuch.shared.utils import sync_lock_context

from .backends import get_stream_backend

if TYPE_CHECKING:
    from aiologbuch.shared.types import (
        AsyncStreamProtocol,
        IOMode,
        SyncStreamBackendType,
        SyncStreamProtocol,
    )


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

    def ensure_correct_mode(self, resource: "_StreamResource", mode: "IOMode"):
        if resource.mode != mode:
            raise

    async def aopen_stream(self, filename: str):
        async with self.lock:
            if (resource := self.resources.get(filename)) is None:
                resource = _StreamResource(filename=filename, mode=IOModeEnum.ASYNC)
                self.resources[filename] = resource

            self.ensure_correct_mode(resource=resource, mode=IOModeEnum.ASYNC)

            resource.reference_count += 1

        await resource.aopen()

    def open_stream(self, filename: str):
        with sync_lock_context(lock=self.lock):
            if (resource := self.resources.get(filename)) is None:
                resource = _StreamResource(filename=filename, mode=IOModeEnum.SYNC)
                self.resources[filename] = resource

            self.ensure_correct_mode(resource=resource, mode=IOModeEnum.SYNC)

            resource.reference_count += 1

        resource.open()

    async def asend_message(self, filename: str, msg: bytes):
        async with self.lock:
            if (resource := self.resources.get(filename)) is None:
                raise RuntimeError(f"{filename!r}'s stream was not initialized")

            self.ensure_correct_mode(resource=resource, mode=IOModeEnum.ASYNC)

        await resource.asend(msg=msg)

    def send_message(self, filename: str, msg: bytes):
        with sync_lock_context(lock=self.lock):
            if (resource := self.resources.get(filename)) is None:
                raise RuntimeError(f"{filename!r}'s stream was not initialized")

            self.ensure_correct_mode(resource=resource, mode=IOModeEnum.SYNC)

        resource.send(msg=msg)

    async def aclose_stream(self, filename: str):
        stream = None

        async with self.lock:
            if (resource := self.resources.get(filename)) is None:
                return

            self.ensure_correct_mode(resource=resource, mode=IOModeEnum.ASYNC)

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

            self.ensure_correct_mode(resource=resource, mode=IOModeEnum.SYNC)

            resource.reference_count -= 1
            if resource.reference_count <= 0:
                stream = self.resources.pop(filename)

        if stream:
            stream.close()


class _StreamResource:
    _filename: str
    _lock: Union[Lock, ThreadLock]
    _stream: Union["AsyncStreamProtocol", "SyncStreamProtocol"]

    reference_count: int
    mode: "IOMode"

    def _async_stream(self):
        backend = get_stream_backend(settings.STREAM_BACKEND)
        return backend(filename=self.filename)

    def _sync_stream(self):
        backend = get_stream_backend(cast("SyncStreamBackendType", IOModeEnum.SYNC))
        return backend(filename=self.filename)

    def __init__(self, filename: str, mode: "IOMode"):
        self._filename = filename

        if mode == IOModeEnum.ASYNC:
            self._lock = Lock()
            self._stream = self._async_stream()
        else:
            self._lock = ThreadLock()
            self._stream = self._sync_stream()

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
        if self.mode != IOModeEnum.ASYNC:
            raise

        async with self.lock:
            await self.stream.open()

    def open(self):
        if self.mode != IOModeEnum.SYNC:
            raise

        with self.lock:
            self.stream.open()

    async def asend(self, msg: bytes):
        if self.mode != IOModeEnum.ASYNC:
            raise

        async with self.lock:
            await self.stream.send(msg)

    def send(self, msg: bytes):
        if self.mode != IOModeEnum.SYNC:
            raise

        with self.lock:
            self.stream.send(msg)

    async def aclose(self):
        if self.mode != IOModeEnum.ASYNC:
            raise

        async with self.lock:
            await self.stream.close()

    def close(self):
        if self.mode != IOModeEnum.SYNC:
            raise

        with self.lock:
            self.stream.close()


resource_manager = _ResourceManager()

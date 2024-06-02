from typing import TYPE_CHECKING

from anyio import Lock

from aiologbuch.shared import STREAM_BACKEND

from .backends import get_stream_backend

if TYPE_CHECKING:
    from aiologbuch.types import StreamProtocol


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

    async def aopen_stream(self, filename: str):
        async with self.lock:
            if (resource := self.resources.get(filename)) is None:
                resource = _StreamResource(filename=filename)
                self.resources[filename] = resource
            resource.reference_count += 1

        await resource.open()

    async def asend_message(self, filename: str, msg: bytes):
        async with self.lock:
            if (resource := self.resources.get(filename)) is None:
                raise RuntimeError(f"{filename!r}'s stream was not initialized")

        await resource.send(msg=msg)

    async def aclose_stream(self, filename: str):
        stream = None

        async with self.lock:
            if resource := self.resources.get(filename):
                resource.reference_count -= 1
                if resource.reference_count <= 0:
                    stream = self.resources.pop(filename)

        if stream:
            await stream.close()


class _StreamResource:
    _lock: Lock
    _filename: str
    _stream: "StreamProtocol"
    reference_count: int

    def __init__(self, filename: str):
        self._lock = Lock()
        self._filename = filename
        self._stream = _Stream(filename=self.filename)
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

    async def open(self):
        async with self.lock:
            await self.stream.open()

    async def send(self, msg: bytes):
        async with self.lock:
            await self.stream.send(msg)

    async def close(self):
        async with self.lock:
            await self.stream.close()


_Stream, resource_manager = get_stream_backend(STREAM_BACKEND), _ResourceManager()

from dataclasses import dataclass
from typing import TYPE_CHECKING

from anyio import Lock

from nlogging.handlers.backends import get_backend

from .base import BaseAsyncHandler

if TYPE_CHECKING:
    from nlogging._types import (
        BackendProtocol,
        FilterProtocol,
        FormatterProtocol,
        MapType,
    )


backend_class = get_backend("aiofile")


@dataclass
class _StreamResource:
    filename: str
    backend: "BackendProtocol | None" = None
    _lock: Lock = None

    def __post_init__(self):
        self._lock = Lock()

    async def init_stream(self):
        async with self._lock:
            if not self.backend:
                self.backend = backend_class(filename=self.filename)
                await self.backend.init()

    async def send(self, msg: bytes):
        async with self._lock:
            if not self.backend:
                raise RuntimeError("Stream is not initialized")
            await self.backend.send(msg)

    async def close(self):
        async with self._lock:
            if self.backend:
                await self.backend.close()
                self.backend = None


@dataclass
class _ResourceManager:
    _map: dict[str, "MapType"] = None
    _lock: Lock = None

    def __post_init__(self):
        self._lock = Lock()
        self._map = {}

    @property
    def map(self):
        return self._map

    async def request_resource(self, filename: str):
        async with self._lock:
            if content := self.map.get(filename):
                resource = content["resource"]
                content["reference_count"] += 1
            else:
                resource = _StreamResource(filename=filename)
                self.map[filename] = {"resource": resource, "reference_count": 1}

        await resource.init_stream()

    async def send_message(self, filename: str, msg: bytes):
        async with self._lock:
            if not (content := self.map.get(filename)):
                raise RuntimeError("Resource is not initialized")

        await content["resource"].send(msg)

    async def close_resource(self, filename: str):
        resource = None

        async with self._lock:
            if content := self.map.get(filename):
                content["reference_count"] -= 1
                if content["reference_count"] <= 0:
                    resource = self.map.pop(filename)["resource"]

        if resource:
            await resource.close()


class AsyncFileHandler(BaseAsyncHandler):
    should_request_resource = True
    _manager = _ResourceManager()

    def __init__(
        self, filename: str, filter: "FilterProtocol", formatter: "FormatterProtocol"
    ):
        if not filename:
            raise ValueError("'filename' cannot be empty")
        super().__init__(filter=filter, formatter=formatter)
        self._filename = filename

    @property
    def filename(self):
        return self._filename

    @property
    def manager(self):
        return self._manager

    async def write_and_flush(self, msg: bytes):
        if self.should_request_resource:
            await self.manager.request_resource(self.filename)
            self.should_request_resource = False

        await self.manager.send_message(self.filename, msg)

    async def close(self):
        await self.manager.close_resource(self.filename)
        self.should_request_resource = True

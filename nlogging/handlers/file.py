from dataclasses import dataclass
from typing import TYPE_CHECKING

from anyio import Lock
from anyio.streams.file import FileWriteStream

from nlogging.handlers.base import BaseAsyncHandler

if TYPE_CHECKING:
    from nlogging._types import FormatterProtocol, LevelType, MapType


@dataclass
class _StreamResource:
    lock: Lock
    filename: str
    stream: FileWriteStream | None = None

    async def init_stream(self):
        async with self.lock:
            if not self.stream:
                self.stream = await FileWriteStream.from_path(self.filename, True)

    async def send(self, msg: bytes):
        async with self.lock:
            if not self.stream:
                raise RuntimeError("Stream is not initialized")
            await self.stream.send(msg)

    async def close(self):
        async with self.lock:
            if self.stream:
                await self.stream.aclose()
                self.stream = None


@dataclass
class _ResourceManager:
    _lock = Lock()
    _map: dict[str, "MapType"] = None

    @property
    def lock(self):
        return self._lock

    @property
    def map(self):
        if not self._map:
            self._map = {}
        return self._map

    async def request_resource(self, filename: str):
        async with self.lock:
            if content := self.map.get(filename):
                resource = content["resource"]
                content["reference_count"] += 1
            else:
                resource = _StreamResource(lock=Lock(), filename=filename)
                self.map[filename] = {"resource": resource, "reference_count": 1}

        await resource.init_stream()

    async def send_message(self, filename: str, msg: bytes):
        async with self.lock:
            if not (content := self.map.get(filename)):
                raise RuntimeError("Resource is not initialized")

        await content["resource"].send(msg)

    async def close_resource(self, filename: str):
        resource = None

        async with self.lock:
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
        self, filename: str, level: "LevelType", formatter: "FormatterProtocol"
    ):
        if not filename:
            raise ValueError("'filename' cannot be empty")
        super().__init__(level=level, formatter=formatter)
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

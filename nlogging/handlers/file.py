from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from anyio import Lock
from anyio.streams.file import FileWriteStream

from .base import BaseAsyncHandler

if TYPE_CHECKING:
    from logging import LogRecord

    from nlogging._types import LevelType
    from nlogging.formatters import BaseFormatter


_resource_map: dict[str, "_StreamResource"] = {}


@dataclass
class _StreamResource:
    lock: Lock
    filename: str
    stream: Optional[FileWriteStream] = None

    async def send(self, msg: bytes):
        async with self.lock:
            if not self.stream:
                self.stream = await FileWriteStream.from_path(
                    path=self.filename, append=True
                )
            await self.stream.send(msg)

    async def close(self):
        global _resource_map

        _resource_map.pop(self.filename, None)

        if self.stream:
            async with self.lock:
                await self.stream.aclose()
                self.stream = None


class AsyncFileHandler(BaseAsyncHandler):
    resource: _StreamResource

    terminator = b"\n"

    def __init__(self, filename: str, level: "LevelType", formatter: "BaseFormatter"):
        if not filename:
            raise ValueError("'filename' cannot be empty")

        super().__init__(level=level, formatter=formatter)

        global _resource_map

        self.resource = _resource_map.get(filename, None)
        if not self.resource:
            _resource_map[filename] = _StreamResource(lock=Lock(), filename=filename)
            self.resource = _resource_map[filename]

    async def emit(self, record: "LogRecord"):
        try:
            msg = self.format(record) + self.terminator
            await self.write_and_flush(msg)
        except:  # noqa
            await self.handle_error(record)

    async def write_and_flush(self, msg: bytes):
        await self.resource.send(msg)

    async def close(self):
        await self.resource.close()

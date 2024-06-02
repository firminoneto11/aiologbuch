from .manager import resource_manager


class AsyncFileMixin:
    _filename: str
    should_open_stream = True

    @property
    def filename(self):
        return self._filename

    @property
    def manager(self):
        return resource_manager

    async def write_and_flush(self, msg: bytes):
        if self.should_open_stream:
            await self.manager.aopen_stream(filename=self.filename)
            self.should_open_stream = False

        await self.manager.asend_message(filename=self.filename, msg=msg)

    async def close(self):
        await self.manager.aclose_stream(filename=self.filename)
        self.should_open_stream = True

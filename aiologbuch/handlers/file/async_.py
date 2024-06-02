from .manager import resource_manager


class AsyncFileMixin:
    _filename: str
    should_request_resource = True

    @property
    def filename(self):
        return self._filename

    @property
    def manager(self):
        return resource_manager

    async def write_and_flush(self, msg: bytes):
        if self.should_request_resource:
            await self.manager.request_resource(self.filename)
            self.should_request_resource = False

        await self.manager.send_message(self.filename, msg)

    async def close(self):
        await self.manager.close_resource(self.filename)
        self.should_request_resource = True

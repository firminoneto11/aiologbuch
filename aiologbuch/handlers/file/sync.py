from .manager import resource_manager


class SyncFileMixin:
    _filename: str
    should_open_stream = True

    @property
    def filename(self):
        return self._filename

    @property
    def manager(self):
        return resource_manager

    def write_and_flush(self, msg: bytes):
        if self.should_open_stream:
            self.manager.open_stream(filename=self.filename)
            self.should_open_stream = False

        self.manager.send_message(filename=self.filename, msg=msg)

    def close(self):
        self.manager.close_stream(filename=self.filename)
        self.should_open_stream = True

import atexit

from .manager import resource_manager


class SyncStreamMixin:
    @property
    def manager(self):
        return resource_manager

    def write_and_flush(self, msg: bytes):
        self.manager.send_message(msg)

    def close(self):
        atexit.register(self.manager.close)

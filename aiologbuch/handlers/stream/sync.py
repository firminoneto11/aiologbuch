import atexit
from typing import TYPE_CHECKING

from .manager import resource_manager

if TYPE_CHECKING:
    from aiologbuch.types import FilterProtocol, FormatterProtocol


class SyncStreamMixin:
    def __init__(self, filter: "FilterProtocol", formatter: "FormatterProtocol"):
        super().__init__(filter=filter, formatter=formatter)

    @property
    def manager(self):
        return resource_manager

    def write_and_flush(self, msg: bytes):
        self.manager.send_message(msg)

    def close(self):
        atexit.register(self.manager.close)

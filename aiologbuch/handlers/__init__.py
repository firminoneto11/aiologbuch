from typing import TYPE_CHECKING as _TypeChecking

from .base import BaseAsyncHandler as _BaseAsync
from .base import BaseSyncHandler as _BaseSync
from .file import AsyncFileMixin as _AsyncFileMixin
from .stream import AsyncStreamMixin as _AsyncStreamMixin
from .stream import SyncStreamMixin as _SyncStreamMixin

# from .file import SyncFileMixin as _SyncFileMixin


if _TypeChecking:
    from aiologbuch.types import FilterProtocol, FormatterProtocol


class AsyncStreamHandler(_BaseAsync, _AsyncStreamMixin):
    ...


class SyncStreamHandler(_BaseSync, _SyncStreamMixin):
    ...


class AsyncFileHandler(_BaseAsync, _AsyncFileMixin):
    def __init__(
        self, filename: str, filter: "FilterProtocol", formatter: "FormatterProtocol"
    ):
        if not filename:
            raise ValueError("'filename' cannot be empty")
        super(_BaseAsync, self).__init__(filter=filter, formatter=formatter)
        self._filename = filename


# class SyncFileHandler(_BaseSync, _SyncFileMixin):
#     ...

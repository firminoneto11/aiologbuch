from typing import TYPE_CHECKING as _TypeChecking

from .base import BaseAsyncHandler as _BaseAsync
from .base import BaseSyncHandler as _BaseSync
from .file import AsyncFileMixin as _AsyncFileMixin
from .stderr import AsyncStderrMixin as _AsyncStderrMixin
from .stderr import SyncStderrMixin as _SyncStderrMixin

if _TypeChecking:
    from aiologbuch.shared.types import FilterProtocol, FormatterProtocol


class AsyncStderrHandler(_BaseAsync, _AsyncStderrMixin):
    ...


class SyncStderrHandler(_BaseSync, _SyncStderrMixin):
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

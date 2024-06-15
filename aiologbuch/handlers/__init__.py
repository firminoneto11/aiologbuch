from typing import TYPE_CHECKING as _TypeChecking

from .base import BaseAsyncHandler as _BaseAsync
from .base import BaseSyncHandler as _BaseSync
from .file import AsyncFileMixin as _AsyncFileMixin
from .file import SyncFileMixin as _SyncFileMixin
from .stderr import AsyncStderrMixin as _AsyncStderrMixin
from .stderr import SyncStderrMixin as _SyncStderrMixin

if _TypeChecking:
    from aiologbuch.shared.types import FormatterProtocol


class AsyncStderrHandler(_BaseAsync, _AsyncStderrMixin):
    ...


class AsyncFileHandler(_BaseAsync, _AsyncFileMixin):
    def __init__(self, filename: str, formatter: "FormatterProtocol"):
        if not filename:
            raise ValueError("'filename' cannot be empty")

        super(_BaseAsync, self).__init__(formatter=formatter)
        self._filename = filename


class SyncStderrHandler(_BaseSync, _SyncStderrMixin):
    ...


class SyncFileHandler(_BaseSync, _SyncFileMixin):
    def __init__(self, filename: str, formatter: "FormatterProtocol"):
        if not filename:
            raise ValueError("'filename' cannot be empty")

        super(_BaseSync, self).__init__(formatter=formatter)
        self._filename = filename

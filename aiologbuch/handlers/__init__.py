from .base import BaseAsyncHandler as _BaseAsync
from .base import BaseSyncHandler as _BaseSync
from .stream import AsyncStreamMixin as _AsyncStreamMixin
from .stream import SyncStreamMixin as _SyncStreamMixin


class AsyncStreamHandler(_BaseAsync, _AsyncStreamMixin):
    ...


class SyncStreamHandler(_BaseSync, _SyncStreamMixin):
    ...

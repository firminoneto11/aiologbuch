from contextlib import asynccontextmanager, contextmanager

from anyio import Lock as AIOLock
from asgiref.sync import async_to_sync

_STDERR_LOCK = AIOLock()


@contextmanager
def sync_stderr_lock():
    async_to_sync(_STDERR_LOCK.acquire)()
    try:
        yield
    finally:
        _STDERR_LOCK.release()


@asynccontextmanager
async def async_stderr_lock():
    await _STDERR_LOCK.acquire()
    try:
        yield
    finally:
        _STDERR_LOCK.release()

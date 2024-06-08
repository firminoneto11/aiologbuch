from asyncio import Lock
from contextlib import asynccontextmanager, contextmanager

from anyio.from_thread import start_blocking_portal

_STDERR_LOCK = Lock()


@contextmanager
def sync_stderr_lock():
    # NOTE: This check is necessary because in high concurrent scenarios the acquire
    # call within the portal could deadlock the entire program, thus, it is not
    # recommended to mix sync with async logger calls.
    if _STDERR_LOCK.locked():
        raise RuntimeError("Can not acquire the lock. Would deadlock")

    with start_blocking_portal() as portal:
        portal.call(_STDERR_LOCK.acquire)

    try:
        yield
    finally:
        if _STDERR_LOCK.locked():
            _STDERR_LOCK.release()


@asynccontextmanager
async def async_stderr_lock():
    await _STDERR_LOCK.acquire()
    try:
        yield
    finally:
        if _STDERR_LOCK.locked():
            _STDERR_LOCK.release()

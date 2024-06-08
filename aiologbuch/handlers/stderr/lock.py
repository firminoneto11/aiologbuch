from asyncio import Lock, get_running_loop
from contextlib import asynccontextmanager, contextmanager
from threading import current_thread

from anyio import WouldBlock
from anyio.from_thread import start_blocking_portal

_STDERR_LOCK = Lock()


def _thread_has_event_loop():
    try:
        get_running_loop()
        return True
    except RuntimeError:
        return False


@contextmanager
def sync_stderr_lock():
    # NOTE: This check is to prevent blocking the thread's event loop since the blocking
    # portal would do so. With this, we not only prevent IO blocking but also prevent
    # any deadlocks that might happen in high concurrent scenarios with many coroutines
    # acquiring and releasing the lock alongside sync logger calls, should the user mix
    # sync and async logging.
    if _thread_has_event_loop():
        raise WouldBlock(
            (
                f"Can not acquire the lock because the {current_thread().name!r} "
                "thread already has an event loop running"
            )
        )

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

from asyncio import Lock, get_running_loop
from contextlib import asynccontextmanager, contextmanager
from functools import wraps

from anyio.from_thread import start_blocking_portal


class WouldDeadlock(Exception):
    def __init__(self):
        message = (
            "Can not acquire the lock because it is currently being used by another "
            "coroutine"
        )
        super().__init__(message)


def _thread_has_event_loop():
    try:
        get_running_loop()
        return True
    except RuntimeError:
        return False


@contextmanager
def sync_lock_context(lock: Lock):
    # NOTE: This if check is to prevent the deadlock that would happen in high
    # concurrent scenarios with many coroutines acquiring and releasing the lock
    # alongside sync logger calls, should the user mix sync logging with async logging.
    if _thread_has_event_loop() and lock.locked():
        raise WouldDeadlock()

    with start_blocking_portal() as portal:
        portal.call(lock.acquire)

    try:
        yield
    finally:
        lock.release()


@asynccontextmanager
async def async_lock_context(lock: Lock):
    await lock.acquire()
    try:
        yield
    finally:
        lock.release()


# TODO: Improve type hint
def syncify(function):
    @wraps(function)
    def _actual_decorator(*args, **kwargs):
        with start_blocking_portal() as portal:
            return portal.call(function, *args, **kwargs)

    return _actual_decorator
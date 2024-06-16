from asyncio import Lock, get_running_loop
from contextlib import contextmanager
from functools import partial, wraps
from typing import Awaitable, Callable

from anyio.from_thread import start_blocking_portal

from .exceptions import WouldDeadlock


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

    # TODO: Check the following case:
    # No event loop and lock is locked. Use a generator to yield control but with the
    # lock being held by it. The other case would be multi threading environment, but
    # that'd be safe because the GIL would be released by the waiting thread, leaving
    # room for the thread that is holding the lock to release it.
    if (not _thread_has_event_loop()) and (lock.locked()):
        ...

    with start_blocking_portal() as portal:
        portal.call(lock.acquire)

    try:
        yield
    finally:
        lock.release()


def syncify[R, **Spec](function: Callable[Spec, Awaitable[R]]):
    @wraps(function)
    def _actual_decorator(*args: Spec.args, **kwargs: Spec.kwargs) -> R:
        func = partial(function, *args, **kwargs)
        with start_blocking_portal() as portal:
            return portal.call(func)

    return _actual_decorator


def parse_bool(value: str):
    val = value.lower().strip()
    if val.isdigit():
        return bool(int(val))
    return val == "true"

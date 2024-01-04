from functools import lru_cache
from os import getenv

from anyio import Lock


def _parse_bool(value: str):
    val = value.lower().strip()
    if val.isdigit():
        return bool(int(val))
    return val == "true"


@lru_cache(maxsize=1)
def get_stderr_lock():
    return Lock()


RAISE_EXCEPTIONS = _parse_bool(getenv("NLOGGING_RAISE_EXCEPTIONS", "true"))

ROOT_LOGGER_NAME = "nlogger"

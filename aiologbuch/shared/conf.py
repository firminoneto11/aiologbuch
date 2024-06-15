from asyncio import Lock
from os import getenv

from .types import AsyncStreamBackendType


def _parse_bool(value: str):
    val = value.lower().strip()
    if val.isdigit():
        return bool(int(val))
    return val == "true"


GLOBAL_STDERR_LOCK = Lock()

RAISE_EXCEPTIONS = _parse_bool(getenv("AIOLOGBUCH_RAISE_EXCEPTIONS", "1"))

STREAM_BACKEND: AsyncStreamBackendType = (
    getenv("AIOLOGBUCH_STREAM_BACKEND", "thread").lower().strip()
)

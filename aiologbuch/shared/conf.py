from asyncio import Lock
from os import getenv
from typing import Literal


def _parse_bool(value: str):
    val = value.lower().strip()
    if val.isdigit():
        return bool(int(val))
    return val == "true"


GLOBAL_STDERR_LOCK = Lock()

RAISE_EXCEPTIONS = _parse_bool(getenv("AIOLOGBUCH_RAISE_EXCEPTIONS", "true"))

STREAM_BACKEND: Literal["thread", "aiofile"] = (
    getenv("AIOLOGBUCH_STREAM_BACKEND", "thread").lower().strip()
)

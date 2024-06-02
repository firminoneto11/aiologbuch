from os import getenv

from anyio import Lock


def _parse_bool(value: str):
    val = value.lower().strip()
    if val.isdigit():
        return bool(int(val))
    return val == "true"


STDERR_LOCK = Lock()

RAISE_EXCEPTIONS = _parse_bool(getenv("NLOGGING_RAISE_EXCEPTIONS", "true"))

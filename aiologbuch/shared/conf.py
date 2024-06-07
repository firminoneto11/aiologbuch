from os import getenv


def _parse_bool(value: str):
    val = value.lower().strip()
    if val.isdigit():
        return bool(int(val))
    return val == "true"


RAISE_EXCEPTIONS = _parse_bool(getenv("AIOLOGBUCH_RAISE_EXCEPTIONS", "true"))

STREAM_BACKEND = getenv("AIOLOGBUCH_STREAM_BACKEND", "thread").lower().strip()

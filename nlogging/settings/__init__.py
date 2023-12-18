from os import getenv


def _parse_bool(value: str):
    val = value.lower().strip()
    if val.isdigit():
        return bool(int(val))
    return val == "true"


raise_exceptions = _parse_bool(getenv("NLOGGING_RAISE_EXCEPTIONS", "true"))

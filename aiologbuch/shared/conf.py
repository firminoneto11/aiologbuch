from asyncio import Lock
from os import getenv

from .types import AsyncStreamBackendType
from .utils import parse_bool


class _Settings:
    GLOBAL_STDERR_LOCK = Lock()

    STREAM_BACKEND: AsyncStreamBackendType = (
        getenv("AIOLOGBUCH_STREAM_BACKEND", "thread").lower().strip()
    )

    RAISE_EXCEPTIONS = parse_bool(getenv("AIOLOGBUCH_RAISE_EXCEPTIONS", "0"))


settings = _Settings()

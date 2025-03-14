from asyncio import Lock
from os import getenv
from threading import Lock as ThreadLock

from .types import AsyncStreamBackendType
from .utils import parse_bool

_settings_lock = ThreadLock()
_configured = False


class _Settings:
    RAISE_EXCEPTIONS = parse_bool(getenv("AIOLOGBUCH_RAISE_EXCEPTIONS", "0"))

    GLOBAL_STDERR_LOCK: Lock
    STREAM_BACKEND: AsyncStreamBackendType

    @property
    def is_configured(self):
        with _settings_lock:
            return _configured

    def configure(self, stream_backend: AsyncStreamBackendType = "thread"):
        global _configured

        with _settings_lock:
            if _configured:
                # NOTE: Once called, the settings can not be changed
                return

            self.GLOBAL_STDERR_LOCK = Lock()
            self.STREAM_BACKEND = stream_backend

            _configured = True


settings = _Settings()

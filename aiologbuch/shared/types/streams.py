from typing import Protocol, Self


class AsyncStreamProtocol(Protocol):
    def __call__(self, filename: str) -> Self:
        ...

    async def open(self) -> None:
        ...

    async def send(self, msg: bytes) -> None:
        ...

    async def close(self) -> None:
        ...


class SyncStreamProtocol(Protocol):
    def __call__(self, filename: str) -> Self:
        ...

    def open(self) -> None:
        ...

    def send(self, msg: bytes) -> None:
        ...

    def close(self) -> None:
        ...


class BinaryFileWrapperProtocol(Protocol):
    async def write(self, msg: bytes) -> None:
        ...

    async def close(self) -> None:
        ...

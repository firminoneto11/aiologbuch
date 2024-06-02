from typing import Protocol, Self


class BackendProtocol(Protocol):
    def __call__(self, filename: str) -> Self:
        ...

    async def open(self) -> None:
        ...

    async def send(self, msg: bytes) -> None:
        ...

    async def close(self) -> None:
        ...


class BinaryFileWrapperProtocol(Protocol):
    async def write(self, msg: bytes) -> None:
        ...

    async def close(self) -> None:
        ...

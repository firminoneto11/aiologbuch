from typing import Protocol, Self, TypedDict


class CallerInfo(TypedDict):
    caller_filename: str
    caller_function_name: str
    caller_line_number: int


class MapType(TypedDict):
    resource: "_ResourceProtocol"
    reference_count: int


class _ResourceProtocol(Protocol):
    async def init_stream(self) -> None:
        ...

    async def send(self, msg: bytes) -> None:
        ...

    async def close(self) -> None:
        ...


class BackendProtocol(Protocol):
    def __call__(self, filename: str) -> Self:
        ...

    async def init(self) -> None:
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

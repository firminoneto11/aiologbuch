from typing import Protocol, Self


class FilterProtocol(Protocol):
    def __call__(self, level: int) -> Self:
        ...

    def filter(self, level: int) -> bool:
        ...

    @property
    def level(self) -> int:
        ...

from asyncio import Protocol


class AIOProtocol(Protocol):
    async def _drain_helper(self):
        ...

from pytest import fixture, mark

from nlogging.manager import AsyncLoggerManagerSingleton

pytestmark = [mark.anyio]


@fixture
def anyio_backend():
    return "asyncio"


@fixture
async def clean_up_manager():
    yield
    await AsyncLoggerManagerSingleton.disable_loggers()

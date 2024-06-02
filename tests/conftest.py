import asyncio

from pytest import fixture
from uvloop import EventLoopPolicy

from aiologbuch.loggers import AsyncLoggerManagerSingleton


@fixture(scope="session", autouse=True)
def event_loop():
    asyncio.set_event_loop_policy(EventLoopPolicy())
    loop = asyncio.new_event_loop()

    yield loop

    if loop.is_running():
        loop.stop()

    loop.run_until_complete(loop.shutdown_asyncgens())
    loop.run_until_complete(loop.shutdown_default_executor())

    loop.close()


@fixture
async def clean_up_manager():
    yield
    await AsyncLoggerManagerSingleton.disable_loggers()

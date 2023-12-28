from pytest import fixture

from nlogging.manager import AsyncLoggerManagerSingleton


@fixture
async def clean_up_manager():
    yield
    await AsyncLoggerManagerSingleton.clean_loggers()

from pytest import fixture

from nlogging.manager import LoggerManagerSingleton


@fixture
async def clean_up_manager():
    yield
    await LoggerManagerSingleton.clean_loggers()

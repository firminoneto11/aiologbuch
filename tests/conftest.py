from pytest import fixture, mark, param

from nlogging.loggers import AsyncLoggerManagerSingleton

pytestmark = [mark.anyio]


@fixture(
    params=[
        param(("asyncio", {"use_uvloop": True}), id="asyncio+uvloop"),
    ]
)
def anyio_backend(request):
    return request.param


@fixture
async def clean_up_manager():
    yield
    await AsyncLoggerManagerSingleton.disable_loggers()

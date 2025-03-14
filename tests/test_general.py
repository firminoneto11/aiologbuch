from asyncio import create_task, sleep

from pytest import mark

from aiologbuch import get_logger


@mark.thing
async def test_line_logger():
    logger = get_logger()

    await logger.info("hello world")


@mark.this
async def test_get_logger():
    logger = get_logger()
    slogger = get_logger(name="sync", kind="sync")

    try:
        raise Exception("oh my my")
    except Exception as exc:
        await logger.exception(exc=exc, msg="Houston, we have a problem")

    await logger.info("Hello world")
    await logger.info({"detail": "hello world 2"})
    await logger.debug("this should not be logged")
    slogger.info("Sync hello world")
    await logger.info("Async hello world")
    slogger.info("Sync hello world 2")
    await logger.info("Async hello world 2")


@mark.bug
async def test_bugging():
    logger = get_logger()
    slogger = get_logger(name="sync", kind="sync")

    create_task(logger.info("you're fucked my guy"))
    await sleep(0.01)

    slogger.info("oh no")  # Deadlocks

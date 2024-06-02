from pytest import mark

from aiologbuch import get_logger


def func(a, b):
    return a / b


async def nested(c, logger):
    try:
        func(5, c)
    except ZeroDivisionError as exc:
        await logger.error("What?!", exc)


@mark.damn
async def test_async_nlogger(clean_up_manager):
    logger = get_logger(name="1", level="DEBUG")

    await logger.debug("debug async msg")
    await logger.info("info async msg")
    await logger.warning("warning async msg")
    await logger.error("error async msg")
    await logger.critical("critical async msg")


@mark.damn
async def test_async_nlogger_with_file_handler(clean_up_manager):
    logger = get_logger(name="2", level="DEBUG", filename="log.log")

    await logger.debug("debug async msg")
    await logger.info("info async msg")
    await logger.warning("warning async msg")
    await logger.error("error async msg")
    await logger.critical("critical async msg")


@mark.damn
async def test_logger_exc(clean_up_manager):
    logger = get_logger(name="3", level="DEBUG")

    await nested(0, logger)

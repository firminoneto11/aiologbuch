from nlogging import get_logger

logger = get_logger(name=__name__, level="DEBUG")


async def test_logger():
    await logger.debug("async logging")
    # await logger.info("this is a info")
    # await logger.warning("this is a warning")
    # await logger.error("this is a error")
    # await logger.critical("this is a critical")

    logger.sDebug("sync logging")


logger.sDebug("sync logging")

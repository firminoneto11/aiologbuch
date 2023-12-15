from nlogging import get_logger


async def test_logger():
    logger = get_logger(name=__name__, level="DEBUG")
    await logger.aDebug("async logging")
    await logger.aInfo("this is a info")
    await logger.aWarning("this is a warning")
    await logger.aError("this is a error")
    await logger.aCritical("this is a critical")
    logger.debug("sync logging")
    logger.debug({"hey": "yo"})

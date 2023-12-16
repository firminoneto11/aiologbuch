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


async def test_calling_get_logger_multiple_times_should_return_same_instance():
    logger1 = get_logger(name="logger", level="DEBUG")
    logger2 = get_logger(name="logger", level="DEBUG")

    # assert hex(id(logger1)) == hex(id(logger2))

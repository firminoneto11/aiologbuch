from nlogging import get_logger


async def test_stuff():
    log = get_logger()
    await log.info({"msg": "info"})
    await log.debug("debug")
    log = get_logger(level="DEBUG")
    await log.debug("debug")

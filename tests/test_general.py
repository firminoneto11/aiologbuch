from pytest import mark

from nlogging.loggers import NLogger, SyncNLogger


@mark.one
def test_sync_nlogger():
    logger = SyncNLogger.create_logger("test_sync_nlogger", "DEBUG")
    logger.debug("test_sync_nlogger")
    logger.info("test_sync_nlogger")
    logger.warning("test_sync_nlogger")
    logger.error("test_sync_nlogger")
    logger.exception("test_sync_nlogger")
    logger.critical("test_sync_nlogger")


@mark.two
async def test_async_file_logging():
    logger = NLogger.create_logger(name="1", level="DEBUG")

    await logger.debug("test_sync_nlogger")
    await logger.info("test_sync_nlogger")
    await logger.warning("test_sync_nlogger")
    await logger.error("test_sync_nlogger")
    await logger.exception("test_sync_nlogger")
    await logger.critical("test_sync_nlogger")

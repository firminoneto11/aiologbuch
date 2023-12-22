from pytest import mark

from nlogging import get_logger
from nlogging.levels import LogLevel
from nlogging.loggers import NLogger
from nlogging.settings import ROOT_LOGGER_NAME


@mark.unit
def test_get_logger_without_name_should_return_default_logger():
    logger = get_logger()

    assert logger.name == ROOT_LOGGER_NAME
    assert logger.level == LogLevel.INFO


@mark.unit
def test_get_logger_with_name_should_return_a_new_logger(clean_up_manager: None):
    default_logger = get_logger()
    new_logger = get_logger(name="new-one")

    assert default_logger.mem_addr != new_logger.mem_addr
    assert new_logger.name == "new-one"
    assert new_logger.level == LogLevel.INFO


@mark.unit
@mark.parametrize(
    argnames="new_level",
    argvalues=(
        LogLevel.DEBUG,
        LogLevel.WARNING,
        LogLevel.ERROR,
        LogLevel.ERROR,
        LogLevel.CRITICAL,
        LogLevel.NOTSET,
    ),
)
def test_get_logger_informing_level_should_only_change_default_logger_level(
    new_level: int,
):
    logger1 = get_logger()
    logger1_level_before = logger1.level == LogLevel.INFO
    logger2 = get_logger(level=new_level)

    assert logger1_level_before
    assert logger1.level == new_level
    assert logger2.level == new_level
    assert logger1.mem_addr == logger2.mem_addr


@mark.unit
@mark.parametrize(
    argnames="name",
    argvalues=(
        "new-one",
        "another-one",
        "one-more",
        "last-one",
    ),
)
def test_get_logger_calling_same_name_should_always_return_same_logger(
    name: str, clean_up_manager: None
):
    assert get_logger(name=name).mem_addr == get_logger(name=name).mem_addr
    assert get_logger().__class__.__name__ == NLogger.__name__


@mark.unit
@mark.parametrize(
    argnames="name",
    argvalues=(
        "new-one",
        "another-one",
        "one-more",
        "last-one",
    ),
)
def test_get_logger_informing_different_level_and_same_name_should_only_change_level(
    name: str, clean_up_manager: None
):
    loggers, assertions, ids = [], [], set()

    for level in LogLevel._member_names_:
        logger = get_logger(name=name, level=level)
        assertions.append(logger.level == LogLevel[level].value)
        ids.add(logger.mem_addr)
        loggers.append(logger)

    assert all(logger.level == LogLevel.NOTSET for logger in loggers)
    assert all(assertions)
    assert len(ids) == 1

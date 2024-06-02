from logging import get_logger
from logging.levels import LogLevel
from logging.loggers import NLogger

from pytest import mark


def mem_addr(obj: object):
    return hex(id(obj))


@mark.unit
def test_get_logger_without_name_should_return_default_logger():
    logger = get_logger(name="log")

    assert logger.name == "log"
    assert logger.level == LogLevel.INFO


@mark.unit
def test_get_logger_with_name_should_return_a_new_logger(clean_up_manager: None):
    default_logger = get_logger(name="log")
    new_logger = get_logger(name="new-one")

    assert mem_addr(default_logger) != mem_addr(new_logger)
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
    ),
)
def test_get_logger_informing_level_should_not_change_logger_level(
    new_level: int,
):
    logger1 = get_logger(name="log")
    logger1_level_before = logger1.level == LogLevel.INFO
    logger2 = get_logger(name="log", level=new_level)

    assert logger1_level_before
    assert logger1.level == LogLevel.INFO
    assert logger2.level == LogLevel.INFO
    assert mem_addr(logger1) == mem_addr(logger2)


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
    assert mem_addr(get_logger(name=name)) == mem_addr(get_logger(name=name))
    assert get_logger(name="log").__class__.__name__ == NLogger.__name__


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
def test_get_logger_informing_different_level_and_same_name_should_change_nothing(
    name: str, clean_up_manager: None
):
    loggers, assertions, ids = [], [], set()

    lowest_level = LogLevel[LogLevel._member_names_[0]]

    for level in LogLevel._member_names_:
        logger = get_logger(name=name, level=level)
        assertions.append(logger.level == lowest_level)
        ids.add(mem_addr(logger))
        loggers.append(logger)

    assert all(logger.level == lowest_level for logger in loggers)
    assert all(assertions)
    assert len(ids) == 1

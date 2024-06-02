from logging.levels import check_level

from pytest import mark, raises


@mark.parametrize(
    argnames="value",
    argvalues=[None, 1.0, (), [], {}, object()],
)
def test_check_level_should_raise_if_level_is_not_int_or_str(value):
    with raises(TypeError) as exc_info:
        check_level(value)

    assert str(exc_info.value) == f"Level not an union of int and str: {value}"

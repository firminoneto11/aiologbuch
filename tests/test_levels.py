from pytest import mark, raises

from nlogging.levels import check_level


@mark.parametrize(
    argnames="value",
    argvalues=[None, True, False, 1.0, (), [], {}],
)
def test_check_level_should_raise_if_level_is_not_int_or_str(value):
    with raises(TypeError) as exc_info:
        check_level(value)

    assert str(exc_info.value) == f"Level not an union of int and str: {value}"

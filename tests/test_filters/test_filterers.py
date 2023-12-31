from collections import namedtuple

from pytest import mark, raises

from nlogging.filters import Filterer


@mark.unit
def test_validate_filter_should_raise_if_object_has_no_id():
    with raises(TypeError) as exc_info:
        Filterer()._validate_filter(filter=object())

    assert str(exc_info.value) == "Filter must have an id attribute"


@mark.unit
def test_validate_filter_should_raise_if_object_has_no_filter_method():
    with raises(TypeError) as exc_info:
        Filterer()._validate_filter(filter=namedtuple("Obj", "id")(id=1), adding=True)

    assert str(exc_info.value) == "Filter must have a filter method"


@mark.unit
def test_validate_filter_should_raise_if_filter_method_is_not_callable():
    with raises(TypeError) as exc_info:
        Filterer()._validate_filter(
            filter=namedtuple("Obj", ("id", "filter"))(id=1, filter=1), adding=True
        )

    assert str(exc_info.value) == "The 'filter' method must be callable"


@mark.unit
def test_validate_filter_should_not_raise_if_object_has_id_and_filter_method():
    Filterer()._validate_filter(
        filter=namedtuple("Obj", ("id", "filter"))(id=1, filter=lambda x: x),
        adding=True,
    )


@mark.unit
def test_validate_filter_should_not_raise_when_adding_is_false():
    Filterer()._validate_filter(filter=namedtuple("Obj", "id")(id=1))


@mark.unit
def test_init_filterer_should_initialize_empty_map():
    assert Filterer().filters == {}


@mark.unit
def test_add_filter_should_add_filter_to_filters_map():
    filterer = Filterer()

    filter_ = namedtuple("Filter", ("id", "filter"))(id="filter_id", filter=lambda x: x)

    filterer.add_filter(filter_)

    assert filterer.filters == {"filter_id": filter_}


@mark.unit
def test_add_filter_should_raise_if_filter_is_not_valid():
    filterer = Filterer()

    with raises(TypeError) as exc_info:
        filterer.add_filter(object())

    assert str(exc_info.value) == "Filter must have an id attribute"


@mark.unit
def test_remove_filter_should_raise_if_filter_is_not_valid():
    filterer = Filterer()

    with raises(TypeError) as exc_info:
        filterer.remove_filter(object())

    assert str(exc_info.value) == "Filter must have an id attribute"


@mark.unit
def test_remove_filter_should_remove_filter_from_filters_map():
    filterer = Filterer()

    filter_ = namedtuple("Filter", ("id", "filter"))(id="filter_id", filter=lambda x: x)

    filterer.add_filter(filter_)

    filters_before = filterer.filters == {"filter_id": filter_}

    filterer.remove_filter(filter_)

    assert filters_before and filterer.filters == {}

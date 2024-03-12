from tap_superset.client_helper import *


def test_update_dict_with():
    source = [{"foo": 1}, {"foo": 2}]
    field = "bar"
    field_list = [3, 4]

    expected = [{"foo": 1, "bar": 3}, {"foo": 2, "bar": 4}]

    result = update_dict_with(source, field, field_list)

    assert expected == result
    assert source != result


def test_get_start_timestamp():
    input = "2022-05-10T19:57:35.680477"
    expected = "2022-05-10 19:57:35.680477"
    result = get_start_timestamp(input)
    assert result == expected


def test_get_start_timestamp_with_none():
    input = None
    expected = None
    result = get_start_timestamp(input)
    assert result == expected

import pytest

from app import process_data


def test_basic_summary():
    records = [{"value": 10}, {"value": 20}, {"value": 30}]
    result = process_data(records)
    assert result["count"] == 3
    assert result["mean"] == 20.0
    assert result["min"] == 10.0
    assert result["max"] == 30.0
    assert result["skipped"] == 0


def test_skips_missing_value_key():
    records = [{"value": 5}, {}]
    result = process_data(records)
    assert result["count"] == 1
    assert result["skipped"] == 1


def test_skips_non_numeric_value():
    records = [{"value": "bad"}, {"value": None}, {"value": 7}]
    result = process_data(records)
    assert result["count"] == 1
    assert result["mean"] == 7.0
    assert result["skipped"] == 2


def test_skips_non_dict_records():
    records = [{"value": 3}, "not a dict", 42]
    result = process_data(records)
    assert result["count"] == 1
    assert result["skipped"] == 2


def test_accepts_string_numbers():
    records = [{"value": "15"}, {"value": "25"}]
    result = process_data(records)
    assert result["count"] == 2
    assert result["mean"] == 20.0


def test_empty_list_returns_none_stats():
    result = process_data([])
    assert result["count"] == 0
    assert result["mean"] is None
    assert result["min"] is None
    assert result["max"] is None


def test_all_invalid_returns_none_stats():
    result = process_data([{"value": "x"}, {}])
    assert result["count"] == 0
    assert result["mean"] is None
    assert result["skipped"] == 2


def test_raises_on_non_list_input():
    with pytest.raises(TypeError, match="records must be a list"):
        process_data({"value": 1})  # type: ignore[arg-type]


def test_single_record():
    result = process_data([{"value": 42}])
    assert result["count"] == 1
    assert result["mean"] == 42.0
    assert result["min"] == 42.0
    assert result["max"] == 42.0

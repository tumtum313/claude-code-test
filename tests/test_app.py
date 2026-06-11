import pytest

from app import process_data


# ---------------------------------------------------------------------------
# Backwards-compatibility — all original tests unchanged
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Default mode still returns ungrouped structure
# ---------------------------------------------------------------------------

def test_default_is_ungrouped_even_with_category_fields():
    records = [{"value": 10, "category": "a"}, {"value": 20, "category": "b"}]
    result = process_data(records)
    assert "groups" not in result
    assert result["count"] == 2
    assert result["mean"] == 15.0


def test_ungrouped_result_has_no_sources_field():
    records = [
        {"value": 10, "source_id": "sys-a"},
        {"value": 20},
    ]
    result = process_data(records)
    assert "sources" not in result


def test_ungrouped_counts_records_regardless_of_category_validity():
    # Category field plays no role in the ungrouped path — all records with a
    # valid value must be counted, whatever their category looks like.
    records = [
        {"value": 10},                     # missing category
        {"value": 20, "category": ""},     # empty string
        {"value": 30, "category": 99},     # non-string
        {"value": 40, "category": "ops"},  # valid — included for comparison
    ]
    result = process_data(records)
    assert result["count"] == 4
    assert result["skipped"] == 0
    assert "groups" not in result


# ---------------------------------------------------------------------------
# Grouped records — valid inputs
# ---------------------------------------------------------------------------

def test_grouped_basic_counts_and_stats():
    records = [
        {"value": 10, "category": "sales"},
        {"value": 20, "category": "sales"},
        {"value": 30, "category": "ops"},
    ]
    result = process_data(records, group_by_category=True)
    assert set(result["groups"]) == {"sales", "ops"}
    assert result["groups"]["sales"]["count"] == 2
    assert result["groups"]["sales"]["mean"] == 15.0
    assert result["groups"]["sales"]["min"] == 10.0
    assert result["groups"]["sales"]["max"] == 20.0
    assert result["groups"]["ops"]["count"] == 1
    assert result["skipped"] == 0


def test_grouped_sources_per_group_and_top_level():
    records = [
        {"value": 10, "category": "sales", "source_id": "erp-01"},
        {"value": 20, "category": "sales", "source_id": "crm-02"},
        {"value": 30, "category": "ops",   "source_id": "erp-01"},
    ]
    result = process_data(records, group_by_category=True)
    assert result["groups"]["sales"]["sources"] == ["crm-02", "erp-01"]
    assert result["groups"]["ops"]["sources"] == ["erp-01"]
    assert result["sources"] == ["crm-02", "erp-01"]


# ---------------------------------------------------------------------------
# Skipped records in grouped mode
# ---------------------------------------------------------------------------

def test_grouped_skips_invalid_values_and_counts_them():
    records = [
        {"value": 10,    "category": "sales"},
        {"value": "bad", "category": "sales"},  # non-numeric string
        {"value": 30,    "category": "ops"},
        {},                                      # missing value key
    ]
    result = process_data(records, group_by_category=True)
    assert result["groups"]["sales"]["count"] == 1
    assert result["groups"]["ops"]["count"] == 1
    assert result["skipped"] == 2


def test_grouped_category_with_only_invalid_values_absent_from_output():
    # A category whose every record is skipped must not appear in groups at all.
    records = [
        {"value": "x", "category": "sales"},
        {"value": 20,  "category": "ops"},
    ]
    result = process_data(records, group_by_category=True)
    assert "sales" not in result["groups"]
    assert result["groups"]["ops"]["count"] == 1
    assert result["skipped"] == 1


def test_grouped_skips_non_dict_records():
    # Non-dict items at the top level are skipped and counted in both paths.
    records = [{"value": 10, "category": "sales"}, "not a dict", 42]
    result = process_data(records, group_by_category=True)
    assert result["groups"]["sales"]["count"] == 1
    assert result["skipped"] == 2


# ---------------------------------------------------------------------------
# Category edge cases: missing, empty, non-string
# ---------------------------------------------------------------------------

def test_missing_category_falls_back_to_uncategorized():
    records = [{"value": 10}, {"value": 20, "category": "sales"}]
    result = process_data(records, group_by_category=True)
    assert result["groups"]["uncategorized"]["count"] == 1
    assert result["groups"]["sales"]["count"] == 1


def test_empty_and_whitespace_category_falls_back_to_uncategorized():
    records = [
        {"value": 10, "category": ""},
        {"value": 20, "category": "   "},
    ]
    result = process_data(records, group_by_category=True)
    assert result["groups"]["uncategorized"]["count"] == 2


def test_non_string_category_falls_back_to_uncategorized():
    records = [
        {"value": 10, "category": 42},
        {"value": 20, "category": None},
        {"value": 30, "category": ["ops"]},
    ]
    result = process_data(records, group_by_category=True)
    assert result["groups"]["uncategorized"]["count"] == 3


def test_category_whitespace_is_stripped():
    records = [
        {"value": 10, "category": "  sales  "},
        {"value": 20, "category": "sales"},
    ]
    result = process_data(records, group_by_category=True)
    assert set(result["groups"]) == {"sales"}
    assert result["groups"]["sales"]["count"] == 2


# ---------------------------------------------------------------------------
# Timestamp validation — obviously malformed values discard field, keep record
# ---------------------------------------------------------------------------

def test_malformed_timestamp_does_not_skip_record():
    records = [
        {"value": 10, "timestamp": "not-a-date"},
        {"value": 20, "timestamp": "yesterday"},
        {"value": 30, "timestamp": "32/13/2024"},
    ]
    result = process_data(records)
    assert result["count"] == 3
    assert result["skipped"] == 0


def test_non_string_timestamp_discards_field_keeps_record():
    records = [
        {"value": 10, "timestamp": 20240115},
        {"value": 20, "timestamp": None},
        {"value": 30, "timestamp": []},
    ]
    result = process_data(records)
    assert result["count"] == 3
    assert result["skipped"] == 0


def test_valid_iso8601_timestamps_accepted():
    records = [
        {"value": 10, "timestamp": "2024-01-15"},
        {"value": 20, "timestamp": "2024-01-15T10:30:00"},
        {"value": 30, "timestamp": "2024-01-15T10:30:00+00:00"},
    ]
    result = process_data(records)
    assert result["count"] == 3
    assert result["skipped"] == 0


def test_malformed_timestamp_keeps_record_in_grouped_mode():
    # Timestamp validation must behave identically regardless of grouping mode.
    records = [
        {"value": 10, "category": "ops", "timestamp": "not-a-date"},
        {"value": 20, "category": "ops", "timestamp": None},
    ]
    result = process_data(records, group_by_category=True)
    assert result["groups"]["ops"]["count"] == 2
    assert result["skipped"] == 0


# ---------------------------------------------------------------------------
# Mixed source systems
# ---------------------------------------------------------------------------

def test_mixed_source_ids_ungrouped_still_counts_all_records():
    records = [
        {"value": 10, "source_id": "erp-01"},
        {"value": 20},
        {"value": 30, "source_id": "crm-02"},
    ]
    result = process_data(records)
    assert result["count"] == 3
    assert "sources" not in result


def test_grouped_mixed_sources_aggregated_at_top_level():
    records = [
        {"value": 10, "category": "a", "source_id": "sys-1"},
        {"value": 20, "category": "b", "source_id": "sys-2"},
        {"value": 30, "category": "a"},
    ]
    result = process_data(records, group_by_category=True)
    assert result["sources"] == ["sys-1", "sys-2"]
    assert result["groups"]["a"]["sources"] == ["sys-1"]
    assert result["groups"]["b"]["sources"] == ["sys-2"]

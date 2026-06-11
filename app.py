import logging
import sys
from collections import defaultdict
from datetime import datetime
from typing import Any

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("app.log"),
    ],
)
logger = logging.getLogger(__name__)


def _stats(values: list[float]) -> dict[str, Any]:
    if not values:
        return {"count": 0, "mean": None, "min": None, "max": None}
    return {
        "count": len(values),
        "mean": sum(values) / len(values),
        "min": min(values),
        "max": max(values),
    }


def process_data(
    records: list[dict[str, Any]],
    *,
    group_by_category: bool = False,
) -> dict[str, Any]:
    """Filter records with a valid numeric 'value' field and return summary stats.

    Records may carry 'category' (str), 'timestamp' (ISO 8601 str, validated but
    not stored), and 'source_id' (surfaced in 'sources' lists). Malformed timestamps
    are discarded but do not invalidate the record. Missing/empty/non-string categories
    fall back to 'uncategorized'.

    Args:
        records: List of dicts. Required key: 'value' (numeric).
        group_by_category: When True, returns per-category summaries.

    Returns:
        Ungrouped (default): {count, mean, min, max, skipped}
        Grouped: {groups: {category: {count, mean, min, max, sources}}, skipped, sources}

    Raises:
        TypeError: If records is not a list.
    """
    if not isinstance(records, list):
        raise TypeError(f"records must be a list, got {type(records).__name__}")

    group_values: dict[str, list[float]] = defaultdict(list)
    group_sources: dict[str, list[str]] = defaultdict(list)
    all_values: list[float] = []
    all_sources: list[str] = []
    skipped = 0

    for i, record in enumerate(records):
        if not isinstance(record, dict):
            logger.warning("Record %d is not a dict, skipping", i)
            skipped += 1
            continue

        raw_value = record.get("value")
        try:
            value = float(raw_value)  # type: ignore[arg-type]
        except (TypeError, ValueError):
            logger.warning("Record %d has invalid value %r, skipping", i, raw_value)
            skipped += 1
            continue

        # Validate timestamp — discard field if malformed, keep the record
        if "timestamp" in record:
            ts = record["timestamp"]
            if not isinstance(ts, str) or not ts.strip():
                logger.warning("Record %d has non-string timestamp %r, ignoring field", i, ts)
            else:
                try:
                    datetime.fromisoformat(ts)
                except ValueError:
                    logger.warning("Record %d has malformed timestamp %r, ignoring field", i, ts)

        # Normalize source_id to a plain string; absent/None produces ""
        raw_source = record.get("source_id")
        source = str(raw_source).strip() if raw_source is not None else ""

        # Normalize category — non-string, empty, or absent falls back to "uncategorized"
        raw_cat = record.get("category")
        if isinstance(raw_cat, str) and raw_cat.strip():
            category = raw_cat.strip()
        else:
            if raw_cat is not None:
                logger.warning("Record %d has invalid category %r, using 'uncategorized'", i, raw_cat)
            category = "uncategorized"

        all_values.append(value)
        all_sources.append(source)
        group_values[category].append(value)
        group_sources[category].append(source)

    logger.info("Processed %d valid records, skipped %d", len(all_values), skipped)

    if group_by_category:
        groups = {}
        for cat in sorted(group_values):
            stats = _stats(group_values[cat])
            stats["sources"] = sorted({s for s in group_sources[cat] if s})
            groups[cat] = stats
        return {
            "groups": groups,
            "skipped": skipped,
            "sources": sorted({s for s in all_sources if s}),
        }

    result = _stats(all_values)
    result["skipped"] = skipped
    return result


def main() -> None:
    sample = [
        {"value": 10, "category": "sales", "timestamp": "2024-01-15T10:00:00", "source_id": "erp-01"},
        {"value": 20, "category": "sales", "timestamp": "2024-01-16T11:30:00", "source_id": "erp-01"},
        {"value": 15, "category": "ops",   "timestamp": "not-a-date",           "source_id": "crm-02"},
        {"value": "bad", "category": "ops",                                      "source_id": "crm-02"},
        {"value": 30, "category": "ops",   "timestamp": "2024-01-17T09:00:00",  "source_id": "crm-02"},
        {"value": 25,                                                             "source_id": "erp-01"},
        {},
    ]

    logger.info("=== Ungrouped ===")
    logger.info(process_data(sample))

    logger.info("=== Grouped by category ===")
    logger.info(process_data(sample, group_by_category=True))


if __name__ == "__main__":
    main()

import logging
import sys
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


def process_data(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Filter records with a valid numeric 'value' field and return summary stats.

    Args:
        records: List of dicts, each expected to contain a 'value' key.

    Returns:
        Dict with keys: count, mean, min, max, skipped.

    Raises:
        TypeError: If records is not a list.
    """
    if not isinstance(records, list):
        raise TypeError(f"records must be a list, got {type(records).__name__}")

    valid: list[float] = []
    skipped = 0

    for i, record in enumerate(records):
        if not isinstance(record, dict):
            logger.warning("Record %d is not a dict, skipping", i)
            skipped += 1
            continue

        raw = record.get("value")
        try:
            valid.append(float(raw))  # type: ignore[arg-type]
        except (TypeError, ValueError):
            logger.warning("Record %d has invalid value %r, skipping", i, raw)
            skipped += 1

    logger.info("Processed %d valid records, skipped %d", len(valid), skipped)

    if not valid:
        return {"count": 0, "mean": None, "min": None, "max": None, "skipped": skipped}

    return {
        "count": len(valid),
        "mean": sum(valid) / len(valid),
        "min": min(valid),
        "max": max(valid),
        "skipped": skipped,
    }


def main() -> None:
    sample = [
        {"value": 10},
        {"value": 20},
        {"value": "bad"},
        {"value": 30},
        {},
    ]
    result = process_data(sample)
    logger.info("Result: %s", result)


if __name__ == "__main__":
    main()

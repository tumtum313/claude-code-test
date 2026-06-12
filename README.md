# claude-code

A production-ready Python data processing application.

## Setup

**Requirements:** Python 3.10+

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Running

```bash
python app.py
```

Logs are written to both stdout and `app.log`.

## Testing

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=app tests/

# Run a single test
pytest tests/test_app.py::test_basic_summary
```

## Project Structure

```
app.py          # Main application — process_data() and entry point
requirements.txt
tests/
    test_app.py # pytest unit tests for process_data()
app.log         # Runtime log output (created on first run)
```

## API

### `process_data(records, group_by_category=False)`

Accepts a list of dicts, each with a numeric `"value"` key. Values may be
numbers or numeric strings. Invalid records are skipped and logged.

By default, returns an ungrouped summary dict:

| Key       | Type           | Description                        |
|-----------|----------------|------------------------------------|
| `count`   | `int`          | Number of valid records processed  |
| `mean`    | `float\|None`  | Arithmetic mean of valid values    |
| `min`     | `float\|None`  | Minimum valid value                |
| `max`     | `float\|None`  | Maximum valid value                |
| `skipped` | `int`          | Number of invalid/skipped records  |

When `group_by_category=True`, returns:

| Key       | Type   | Description                                  |
|-----------|--------|----------------------------------------------|
| `groups`  | `dict` | Per-category summary stats and source IDs    |
| `skipped` | `int`  | Number of invalid/skipped records            |
| `sources` | `list` | Sorted unique non-empty source IDs observed  |

Optional record fields:

| Field       | Type  | Behavior                                           |
|-------------|-------|----------------------------------------------------|
| `category`  | `str` | Used for grouped output; blank or invalid values fall back to `uncategorized` |
| `timestamp` | `str` | Validated as ISO 8601 when present; malformed timestamps are logged but do not skip the record |
| `source_id` | `any` | Converted to a trimmed string and included in grouped source lists when non-empty |

Records missing `"value"`, with non-numeric values, or that are not dicts are
skipped and logged as warnings.

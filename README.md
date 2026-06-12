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

### `process_data(records)`

Accepts a list of dicts, each with a numeric `"value"` key. Returns a summary dict:

| Key       | Type           | Description                        |
|-----------|----------------|------------------------------------|
| `count`   | `int`          | Number of valid records processed  |
| `mean`    | `float\|None`  | Arithmetic mean of valid values    |
| `min`     | `float\|None`  | Minimum valid value                |
| `max`     | `float\|None`  | Maximum valid value                |
| `skipped` | `int`          | Number of invalid/skipped records  |

Records missing `"value"`, with non-numeric values, or that are not dicts are skipped and logged as warnings.

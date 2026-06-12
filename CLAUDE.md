# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Status

This repository contains a Python data processing application in `app.py` with
pytest coverage in `tests/test_app.py`.

## Setup

Requires Python 3.10+.

```bash
python -m pip install -r requirements.txt
```

## Test Commands

```bash
python -m pytest
python -m pytest --cov=app tests/
```

## Architecture Notes

- `app.py` exposes `process_data(records, group_by_category=False)`.
- The default mode returns ungrouped summary statistics: `count`, `mean`, `min`,
  `max`, and `skipped`.
- Grouped mode returns per-category statistics, top-level skipped count, and
  source identifiers.
- Invalid records are skipped and logged. Malformed timestamps are logged but do
  not invalidate otherwise valid records.

## Git LFS

This repository is configured for Git LFS. Ensure `git-lfs` is installed before pushing, or the pre-push hook will block the push.

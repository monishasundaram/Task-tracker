"""JSON file storage with safe handling of missing or corrupt files."""

import json
from pathlib import Path


class StorageError(Exception):
    """Raised when the data file cannot be read or written."""


def load_tasks(path: Path) -> list[dict]:
    """Return the list of raw task dicts, or an empty list if the file does not exist."""
    path = Path(path)
    if not path.exists():
        return []
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as exc:
        raise StorageError(f"Data file '{path}' is corrupt: {exc}") from exc
    except OSError as exc:
        raise StorageError(f"Could not read '{path}': {exc}") from exc
    if not isinstance(data, list):
        raise StorageError(f"Data file '{path}' has an unexpected format.")
    return data


def save_tasks(path: Path, tasks: list[dict]) -> None:
    """Write tasks to disk atomically so a crash cannot leave a half-written file."""
    path = Path(path)
    tmp = path.with_suffix(path.suffix + ".tmp")
    try:
        with tmp.open("w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=2)
        tmp.replace(path)
    except OSError as exc:
        raise StorageError(f"Could not write '{path}': {exc}") from exc

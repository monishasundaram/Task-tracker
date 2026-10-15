# Task Tracker (Core Concepts and Skills Mini-Project)

A small command-line task manager built to demonstrate the core concepts from the
**Core Concepts and Skills** phase: clean structure, data modelling, validation,
error handling, file persistence, testing, and documentation.

## Features

- Add tasks with a priority (`low`, `medium`, `high`)
- List all tasks, only pending tasks, or filter by priority
- Mark tasks as done or delete them
- See a progress summary
- Data is saved to a JSON file, so tasks persist between runs

## Getting Started

Requires Python 3.10 or newer.

```bash
git clone https://github.com/<your-username>/task-tracker.git
cd task-tracker
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

```bash
python -m tracker add "Finish quiz" -p high
python -m tracker add "Read tutorial chapter 3"
python -m tracker list
python -m tracker list --pending
python -m tracker done 1
python -m tracker stats
python -m tracker delete 2
```

Example output:

```
[ ] #1   high   Finish quiz
[ ] #2   medium Read tutorial chapter 3
Total: 2 | Done: 0 | Pending: 2 | 0.0% complete
```

By default tasks are stored in `~/.task_tracker.json`. Use `--file path.json` to choose another file.

## Running the Tests

```bash
python -m pytest
```

## Project Structure

```
task-tracker/
├── tracker/
│   ├── models.py     # Task dataclass and validation
│   ├── storage.py    # JSON read/write with error handling
│   ├── manager.py    # Business logic (add, complete, delete, list, stats)
│   └── cli.py        # Command-line interface (argparse)
├── tests/
│   └── test_tracker.py
├── requirements.txt
├── .gitignore
└── LICENSE
```

## Concepts Demonstrated

| Concept | Where it appears |
|---|---|
| Separation of concerns | Model, storage, logic and interface are in separate modules |
| Data modelling | `Task` dataclass in `models.py` |
| Input validation | Empty titles and invalid priorities are rejected |
| Error handling | Custom exceptions; the CLI shows friendly messages instead of crashes |
| File I/O and persistence | Atomic JSON saves in `storage.py` |
| Sorting and filtering | `TaskManager.list()` |
| Testing | 12 automated pytest tests covering logic, storage and the CLI |
| Documentation | Docstrings, type hints and this README |

## Common Pitfalls Avoided

- **Crashing on a missing data file:** a missing file is treated as an empty task list.
- **Corrupt data:** invalid JSON raises a clear `StorageError` rather than a raw traceback.
- **Half-written files:** saves go to a temporary file first, then replace the original.
- **Reused IDs after deletion:** new IDs are based on the highest existing ID.
- **Division by zero in stats:** an empty list returns 0.0% instead of failing.
- **Tests touching real data:** tests use temporary files only.

## What I Learned

_Add your own reflection here (2 to 3 sentences): what was hardest, what you would improve next._

## Possible Next Steps

- Due dates and reminders
- Edit existing tasks
- Export to CSV
- A simple web interface

## License

MIT. See `LICENSE`.

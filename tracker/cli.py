"""Command-line interface for the Task Tracker."""

import argparse
import sys
from pathlib import Path

from .manager import TaskManager, TaskNotFoundError
from .models import ValidationError
from .storage import StorageError

DEFAULT_FILE = Path.home() / ".task_tracker.json"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tracker", description="A simple command-line task tracker.")
    parser.add_argument("--file", type=Path, default=DEFAULT_FILE, help="path to the data file")
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="add a new task")
    add.add_argument("title")
    add.add_argument("-p", "--priority", default="medium", help="low, medium or high")

    lst = sub.add_parser("list", help="list tasks")
    lst.add_argument("--pending", action="store_true", help="hide completed tasks")
    lst.add_argument("-p", "--priority", help="filter by priority")

    done = sub.add_parser("done", help="mark a task as complete")
    done.add_argument("id", type=int)

    delete = sub.add_parser("delete", help="delete a task")
    delete.add_argument("id", type=int)

    sub.add_parser("stats", help="show progress summary")
    return parser


def format_task(task) -> str:
    mark = "x" if task.done else " "
    return f"[{mark}] #{task.id:<3} {task.priority:<6} {task.title}"


def run(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        manager = TaskManager(args.file)

        if args.command == "add":
            task = manager.add(args.title, args.priority)
            print(f"Added: {format_task(task)}")
        elif args.command == "list":
            tasks = manager.list(show_done=not args.pending, priority=args.priority)
            if not tasks:
                print("No tasks found.")
            for task in tasks:
                print(format_task(task))
        elif args.command == "done":
            print(f"Completed: {format_task(manager.complete(args.id))}")
        elif args.command == "delete":
            print(f"Deleted: {format_task(manager.delete(args.id))}")
        elif args.command == "stats":
            s = manager.stats()
            print(f"Total: {s['total']} | Done: {s['done']} | Pending: {s['pending']} | {s['percent_done']}% complete")
    except (ValidationError, TaskNotFoundError, StorageError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


def main() -> None:
    sys.exit(run())

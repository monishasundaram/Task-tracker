"""Business logic: add, complete, delete, filter and summarise tasks."""

from pathlib import Path

from .models import Task
from .storage import load_tasks, save_tasks

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


class TaskNotFoundError(LookupError):
    """Raised when a task ID does not exist."""


class TaskManager:
    def __init__(self, path: Path):
        self.path = Path(path)
        self.tasks: list[Task] = [Task.from_dict(d) for d in load_tasks(self.path)]

    def _save(self) -> None:
        save_tasks(self.path, [t.to_dict() for t in self.tasks])

    def _next_id(self) -> int:
        return max((t.id for t in self.tasks), default=0) + 1

    def get(self, task_id: int) -> Task:
        for task in self.tasks:
            if task.id == task_id:
                return task
        raise TaskNotFoundError(f"No task with ID {task_id}.")

    def add(self, title: str, priority: str = "medium") -> Task:
        task = Task(id=self._next_id(), title=title, priority=priority)
        self.tasks.append(task)
        self._save()
        return task

    def complete(self, task_id: int) -> Task:
        task = self.get(task_id)
        task.done = True
        self._save()
        return task

    def delete(self, task_id: int) -> Task:
        task = self.get(task_id)
        self.tasks.remove(task)
        self._save()
        return task

    def list(self, show_done: bool = True, priority: str | None = None) -> list[Task]:
        result = [
            t for t in self.tasks
            if (show_done or not t.done) and (priority is None or t.priority == priority)
        ]
        return sorted(result, key=lambda t: (t.done, PRIORITY_ORDER[t.priority], t.id))

    def stats(self) -> dict:
        total = len(self.tasks)
        done = sum(t.done for t in self.tasks)
        return {
            "total": total,
            "done": done,
            "pending": total - done,
            "percent_done": round(100 * done / total, 1) if total else 0.0,
        }

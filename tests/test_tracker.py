import json

import pytest

from tracker.cli import run
from tracker.manager import TaskManager, TaskNotFoundError
from tracker.models import Task, ValidationError
from tracker.storage import StorageError, load_tasks


@pytest.fixture
def manager(tmp_path):
    return TaskManager(tmp_path / "tasks.json")


def test_add_assigns_incrementing_ids(manager):
    assert manager.add("First").id == 1
    assert manager.add("Second").id == 2


def test_tasks_persist_between_sessions(tmp_path):
    path = tmp_path / "tasks.json"
    TaskManager(path).add("Write report", "high")
    reloaded = TaskManager(path)
    assert reloaded.tasks[0].title == "Write report"
    assert reloaded.tasks[0].priority == "high"


def test_empty_title_rejected():
    with pytest.raises(ValidationError):
        Task(id=1, title="   ")


def test_invalid_priority_rejected(manager):
    with pytest.raises(ValidationError):
        manager.add("Task", "urgent")


def test_complete_and_stats(manager):
    manager.add("A")
    manager.add("B")
    manager.complete(1)
    assert manager.stats() == {"total": 2, "done": 1, "pending": 1, "percent_done": 50.0}


def test_stats_with_no_tasks(manager):
    assert manager.stats()["percent_done"] == 0.0


def test_list_sorts_by_priority_and_hides_done(manager):
    manager.add("low one", "low")
    manager.add("high one", "high")
    manager.add("finished", "high")
    manager.complete(3)
    titles = [t.title for t in manager.list(show_done=False)]
    assert titles == ["high one", "low one"]


def test_delete_removes_task(manager):
    manager.add("Temp")
    manager.delete(1)
    assert manager.tasks == []


def test_missing_task_raises(manager):
    with pytest.raises(TaskNotFoundError):
        manager.complete(99)


def test_corrupt_file_raises_storage_error(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text("{not valid json")
    with pytest.raises(StorageError):
        load_tasks(path)


def test_cli_add_and_list(tmp_path, capsys):
    f = str(tmp_path / "t.json")
    assert run(["--file", f, "add", "Buy milk", "-p", "high"]) == 0
    assert run(["--file", f, "list"]) == 0
    assert "Buy milk" in capsys.readouterr().out


def test_cli_reports_error_for_unknown_id(tmp_path, capsys):
    code = run(["--file", str(tmp_path / "t.json"), "done", "5"])
    assert code == 1
    assert "No task with ID 5" in capsys.readouterr().err

"""Data model for a task, with input validation."""

from dataclasses import dataclass, field, asdict
from datetime import datetime

VALID_PRIORITIES = ("low", "medium", "high")


class ValidationError(ValueError):
    """Raised when task data is invalid."""


@dataclass
class Task:
    id: int
    title: str
    priority: str = "medium"
    done: bool = False
    created: str = field(default_factory=lambda: datetime.now().isoformat(timespec="seconds"))

    def __post_init__(self):
        self.title = self.title.strip()
        self.priority = self.priority.lower()
        if not self.title:
            raise ValidationError("Task title cannot be empty.")
        if self.priority not in VALID_PRIORITIES:
            raise ValidationError(
                f"Priority must be one of {', '.join(VALID_PRIORITIES)} (got '{self.priority}')."
            )

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        return cls(
            id=data["id"],
            title=data["title"],
            priority=data.get("priority", "medium"),
            done=data.get("done", False),
            created=data.get("created", datetime.now().isoformat(timespec="seconds")),
        )

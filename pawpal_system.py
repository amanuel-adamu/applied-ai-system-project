"""PawPal+ — backend logic layer.

Core implementation for the smart pet care management system.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import List

# Ordering used to sort tasks by priority (lower value = higher priority).
# Unknown priorities sort last.
PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


@dataclass
class Owner:
    name: str
    pets: List["Pet"] = field(default_factory=list)

    def add_pet(self, pet: "Pet") -> None:
        """Register a pet with this owner, keeping both sides of the link in sync."""
        if pet not in self.pets:
            self.pets.append(pet)
        pet.owner = self

    def view_all_pets(self) -> List["Pet"]:
        """Return the list of pets owned by this owner."""
        return self.pets

    def get_all_tasks(self) -> List["Task"]:
        """Aggregate every task across all pets owned by this owner."""
        tasks: List["Task"] = []
        for pet in self.pets:
            tasks.extend(pet.tasks)
        return tasks


@dataclass
class Pet:
    name: str
    species: str
    owner: Owner
    tasks: List["Task"] = field(default_factory=list)

    def add_task(self, task: "Task") -> None:
        """Attach a task to this pet, keeping the task's back-reference in sync."""
        task.pet = self
        if task not in self.tasks:
            self.tasks.append(task)

    def get_details(self) -> str:
        """Return a human-readable summary of the pet."""
        return (
            f"{self.name} ({self.species}) — owner: {self.owner.name}, "
            f"{len(self.tasks)} task(s)"
        )


@dataclass
class Task:
    title: str
    description: str
    due_date: date
    priority: str
    status: str
    pet: Pet

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.status = "completed"

    def update_priority(self, new_priority: str) -> None:
        """Change the task's priority level."""
        self.priority = new_priority


@dataclass
class Scheduler:
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Register a task with the scheduler."""
        if task not in self.tasks:
            self.tasks.append(task)

    def add_tasks_from_owner(self, owner: Owner) -> None:
        """Pull every task belonging to an owner's pets into the scheduler."""
        for task in owner.get_all_tasks():
            self.add_task(task)

    def get_tasks_by_date(self, target_date: date) -> List[Task]:
        """Return all tasks due on the given date."""
        return [task for task in self.tasks if task.due_date == target_date]

    def sort_tasks_by_priority(self) -> List[Task]:
        """Return tasks sorted by priority (high first); unknown priorities last."""
        return sorted(
            self.tasks,
            key=lambda task: PRIORITY_ORDER.get(task.priority.lower(), len(PRIORITY_ORDER)),
        )

"""PawPal+ — backend logic layer.

Class skeleton for the smart pet care management system.
Method bodies are left as stubs (`pass`) to be implemented later.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import List


@dataclass
class Owner:
    name: str
    pets: List["Pet"] = field(default_factory=list)

    def add_pet(self, pet: "Pet") -> None:
        pass

    def view_all_pets(self) -> None:
        pass


@dataclass
class Pet:
    name: str
    species: str
    owner: Owner

    def get_details(self) -> None:
        pass


@dataclass
class Task:
    title: str
    description: str
    due_date: date
    priority: str
    status: str

    def mark_complete(self) -> None:
        pass

    def update_priority(self, new_priority: str) -> None:
        pass


@dataclass
class Scheduler:
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass

    def get_tasks_by_date(self, date: date) -> None:
        pass

    def sort_tasks_by_priority(self) -> None:
        pass

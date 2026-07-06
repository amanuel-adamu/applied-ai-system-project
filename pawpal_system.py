"""PawPal+ — backend logic layer.

Core implementation for the smart pet care management system.
"""


from __future__ import annotations

from collections import defaultdict
from typing import List
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
    time: str = "00:00"  # 'HH:MM' 24-hour clock
    recurrence: str = "none"  # "none", "daily", or "weekly"
    interval: int = 1        # Every N days/weeks

    def mark_complete(self) -> None:
        """Mark this task as completed and spawn its next occurrence, if recurring.

        Sets ``status`` to ``"completed"``. If this task recurs (``recurrence``
        is not ``"none"``), a fresh pending task for the next date is generated
        via :meth:`next_occurrence` and attached to the same pet, so recurring
        chores automatically roll forward when finished.

        Side effects:
            Mutates ``self.status`` and, for recurring tasks, appends a new
            :class:`Task` to ``self.pet.tasks``.
        """
        self.status = "completed"
        
        # Automatically generate and add the next occurrence to the pet's tasks
        next_task = self.next_occurrence()
        if next_task:
            self.pet.add_task(next_task)

    def next_occurrence(self) -> Task | None:
        """Build the next task in this recurrence series, or ``None`` if one-off.

        Computes the next due date by advancing ``due_date`` by ``interval``
        days (``recurrence == "daily"``) or ``interval`` weeks (any other
        recurring value, treated as weekly). The returned task copies the
        title, description, time, and recurrence settings, but resets
        ``status`` to ``"pending"`` so it appears as unfinished work.

        Returns:
            A new :class:`Task` for the next scheduled date, or ``None`` when
            ``recurrence`` is ``"none"`` (nothing to repeat). This method has
            no side effects; the caller is responsible for scheduling the
            returned task.
        """
        if self.recurrence == "none":
            return None
            
        from datetime import timedelta
        # Calculate the next date
        step = timedelta(days=self.interval) if self.recurrence == "daily" else timedelta(weeks=self.interval)
        
        return Task(
            title=self.title,
            description=self.description,
            due_date=self.due_date + step,
            priority=self.priority,
            status="pending",
            pet=self.pet,
            time=self.time,
            recurrence=self.recurrence,
            interval=self.interval
        )

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

    def sort_by_time(self) -> List[Task]:
        """Return the scheduled tasks ordered chronologically by time of day.

        Uses ``sorted()`` with a lambda key that reads each task's ``time``
        attribute. Zero-padded 24-hour ``'HH:MM'`` strings compare correctly
        as plain strings (``"09:00" < "14:30"``), so no parsing into time
        objects is required. Assumes hours are two digits; an un-padded value
        like ``"9:00"`` would sort out of order.

        Returns:
            A new list of :class:`Task` sorted earliest-first. ``self.tasks``
            is left unmodified.
        """
        return sorted(self.tasks, key=lambda task: task.time)

    def filter_by_status(self, status: str) -> List[Task]:
        """Return only the tasks matching the given status (e.g. 'pending')."""
        return [task for task in self.tasks if task.status == status]

    def filter_by_pet_name(self, pet_name: str) -> List[Task]:
        """Return only the tasks belonging to the pet with the given name."""
        return [task for task in self.tasks if task.pet.name == pet_name]
    def check_conflicts(self) -> List[str]:
        """Detect scheduling collisions and return them as warning messages.

        Groups all pending tasks into ``(due_date, time)`` slots and reports
        two kinds of collision:

        * **Hard conflict** — the same pet has more than one task in a single
          slot (physically impossible; the pet can't be in two places at once).
        * **Soft conflict** — two or more *different* pets share a slot, meaning
          the owner is double-booked and must split their attention.

        Completed tasks are ignored so finished work never raises a warning.
        Both conflict types are reported independently, so a slot can produce
        both a hard and a soft warning. Detection is by exact time match, not
        duration overlap.

        Returns:
            A list of human-readable warning strings, empty when no conflicts
            exist. This method never raises, so callers can surface the
            warnings and keep running.
        """
        warnings: List[str] = []
        # (due_date, time) -> {pet_name: [titles]}
        slots = defaultdict(lambda: defaultdict(list))

        for task in self.tasks:
            if task.status == "completed":
                continue
            slots[(task.due_date, task.time)][task.pet.name].append(task.title)

        for (slot_date, slot_time), pets in slots.items():
            # Hard conflict: one pet with two tasks at the same instant (impossible).
            for pet_name, titles in pets.items():
                if len(titles) > 1:
                    warnings.append(
                        f"Hard conflict: {pet_name} has overlapping tasks "
                        f"({', '.join(titles)}) on {slot_date} at {slot_time}!"
                    )
            # Soft conflict: you're split across multiple pets at the same time.
            if len(pets) > 1:
                warnings.append(
                    f"Conflict warning: you are double-booked on {slot_date} "
                    f"at {slot_time} across {', '.join(pets.keys())}."
                )

        return warnings
"""Ensures the project root is importable so tests can `import pawpal_system`.

Also provides shared pytest fixtures/factories used across the suite to keep the
individual tests focused on behavior rather than object construction.
"""

from __future__ import annotations

from datetime import date

import pytest

from pawpal_system import Owner, Pet, Scheduler, Task


@pytest.fixture
def owner() -> Owner:
    """A fresh owner with no pets."""
    return Owner("Alex")


@pytest.fixture
def pet(owner: Owner) -> Pet:
    """A dog belonging to `owner`, already linked on both sides."""
    p = Pet("Rex", "dog", owner)
    owner.add_pet(p)
    return p


@pytest.fixture
def make_task(pet: Pet):
    """Factory for building tasks attached to the default `pet`.

    Returns a callable so each test can create as many tasks as it needs with
    only the fields it cares about, e.g. ``make_task(time="09:00")``.
    """

    def _make(
        title: str = "Morning walk",
        *,
        description: str = "30 minute walk around the block",
        due_date: date = date(2026, 7, 5),
        priority: str = "high",
        status: str = "pending",
        time: str = "08:00",
        recurrence: str = "none",
        interval: int = 1,
        target_pet: Pet | None = None,
    ) -> Task:
        return Task(
            title=title,
            description=description,
            due_date=due_date,
            priority=priority,
            status=status,
            pet=target_pet if target_pet is not None else pet,
            time=time,
            recurrence=recurrence,
            interval=interval,
        )

    return _make


@pytest.fixture
def scheduler() -> Scheduler:
    """An empty scheduler."""
    return Scheduler()

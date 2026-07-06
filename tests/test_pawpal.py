"""Quick tests for the PawPal+ backend logic."""

from datetime import date

from pawpal_system import Owner, Pet, Task


def _make_task(pet: Pet) -> Task:
    return Task(
        title="Morning walk",
        description="30 minute walk around the block",
        due_date=date(2026, 7, 5),
        priority="High",
        status="pending",
        pet=pet,
    )


def test_task_completion():
    owner = Owner("Alex")
    pet = Pet("Rex", "dog", owner)
    task = _make_task(pet)

    task.mark_complete()

    assert task.status == "completed"


def test_task_addition_increases_pet_task_count():
    owner = Owner("Alex")
    pet = Pet("Rex", "dog", owner)
    assert len(pet.tasks) == 0

    pet.add_task(_make_task(pet))

    assert len(pet.tasks) == 1

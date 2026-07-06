"""Automated test suite for the PawPal+ backend logic.

Covers happy paths and edge cases for tasks, recurrence, scheduling, sorting,
filtering, conflict detection, and owner/pet relationships. Shared fixtures
(`owner`, `pet`, `make_task`, `scheduler`) live in ``conftest.py``.
"""

from datetime import date

from pawpal_system import Owner, Pet


# ---------------------------------------------------------------------------
# Task completion & recurrence logic
# ---------------------------------------------------------------------------

def test_task_completion_sets_status(make_task):
    task = make_task()
    task.mark_complete()
    assert task.status == "completed"


def test_non_recurring_complete_does_not_spawn(make_task, pet):
    task = make_task(recurrence="none")
    pet.add_task(task)
    task.mark_complete()
    # Only the original task should remain; nothing new spawned.
    assert len(pet.tasks) == 1


def test_daily_recurrence_spawns_next_day(make_task, pet):
    """Marking a daily task complete creates a new task for the following day."""
    task = make_task(due_date=date(2026, 7, 5), recurrence="daily", interval=1)
    pet.add_task(task)

    task.mark_complete()

    assert len(pet.tasks) == 2
    spawned = pet.tasks[-1]
    assert spawned.due_date == date(2026, 7, 6)
    assert spawned.status == "pending"
    assert spawned.pet is pet


def test_daily_recurrence_respects_interval(make_task):
    task = make_task(due_date=date(2026, 7, 5), recurrence="daily", interval=3)
    nxt = task.next_occurrence()
    assert nxt.due_date == date(2026, 7, 8)


def test_weekly_recurrence_advances_seven_days(make_task):
    task = make_task(due_date=date(2026, 7, 5), recurrence="weekly", interval=1)
    nxt = task.next_occurrence()
    assert nxt.due_date == date(2026, 7, 12)


def test_weekly_recurrence_respects_interval(make_task):
    task = make_task(due_date=date(2026, 7, 5), recurrence="weekly", interval=2)
    nxt = task.next_occurrence()
    assert nxt.due_date == date(2026, 7, 19)


def test_next_occurrence_none_for_one_off(make_task):
    task = make_task(recurrence="none")
    assert task.next_occurrence() is None


def test_next_occurrence_copies_fields_and_resets_status(make_task):
    task = make_task(
        title="Feed",
        description="dinner",
        priority="low",
        status="completed",
        time="18:30",
        recurrence="daily",
        interval=2,
    )
    nxt = task.next_occurrence()
    assert nxt.title == "Feed"
    assert nxt.description == "dinner"
    assert nxt.priority == "low"
    assert nxt.time == "18:30"
    assert nxt.recurrence == "daily"
    assert nxt.interval == 2
    assert nxt.status == "pending"  # reset even though source was completed


def test_next_occurrence_has_no_side_effects(make_task, pet):
    task = make_task(recurrence="daily")
    pet.add_task(task)
    before = len(pet.tasks)
    task.next_occurrence()  # should not attach anything on its own
    assert len(pet.tasks) == before


def test_recurrence_handles_month_rollover(make_task):
    task = make_task(due_date=date(2026, 12, 31), recurrence="daily", interval=1)
    nxt = task.next_occurrence()
    assert nxt.due_date == date(2027, 1, 1)


def test_unknown_recurrence_treated_as_weekly(make_task):
    """KNOWN BEHAVIOR: any recurring value other than 'daily' falls into the
    weekly branch, so 'monthly' advances by one week, not one month."""
    task = make_task(due_date=date(2026, 7, 5), recurrence="monthly", interval=1)
    nxt = task.next_occurrence()
    assert nxt.due_date == date(2026, 7, 12)


def test_update_priority(make_task):
    task = make_task(priority="low")
    task.update_priority("high")
    assert task.priority == "high"


# ---------------------------------------------------------------------------
# Sorting correctness
# ---------------------------------------------------------------------------

def test_sort_by_time_chronological(make_task, scheduler):
    """Tasks are returned in chronological order by time of day."""
    t_late = make_task(title="late", time="14:30")
    t_early = make_task(title="early", time="08:15")
    t_mid = make_task(title="mid", time="12:00")
    for t in (t_late, t_early, t_mid):
        scheduler.add_task(t)

    ordered = scheduler.sort_by_time()

    assert [t.time for t in ordered] == ["08:15", "12:00", "14:30"]


def test_sort_by_time_does_not_mutate_source(make_task, scheduler):
    scheduler.add_task(make_task(time="14:30"))
    scheduler.add_task(make_task(time="08:15"))
    original = list(scheduler.tasks)
    scheduler.sort_by_time()
    assert scheduler.tasks == original  # returns a new list, source untouched


def test_sort_by_priority(make_task, scheduler):
    low = make_task(title="low", priority="low")
    high = make_task(title="high", priority="high")
    med = make_task(title="med", priority="medium")
    for t in (low, high, med):
        scheduler.add_task(t)

    ordered = scheduler.sort_tasks_by_priority()

    assert [t.priority for t in ordered] == ["high", "medium", "low"]


def test_sort_by_priority_is_case_insensitive(make_task, scheduler):
    scheduler.add_task(make_task(title="a", priority="LOW"))
    scheduler.add_task(make_task(title="b", priority="High"))
    ordered = scheduler.sort_tasks_by_priority()
    assert ordered[0].priority == "High"


def test_sort_by_priority_unknown_sorts_last(make_task, scheduler):
    scheduler.add_task(make_task(title="unknown", priority="urgent"))
    scheduler.add_task(make_task(title="known", priority="high"))
    ordered = scheduler.sort_tasks_by_priority()
    assert ordered[-1].priority == "urgent"


def test_sorting_empty_scheduler(scheduler):
    assert scheduler.sort_by_time() == []
    assert scheduler.sort_tasks_by_priority() == []


def test_unpadded_time_sorts_incorrectly(make_task, scheduler):
    """KNOWN LIMITATION: times are compared as plain strings, so an un-padded
    value like '9:00' sorts AFTER '14:30'. Callers must zero-pad hours."""
    scheduler.add_task(make_task(title="a", time="9:00"))
    scheduler.add_task(make_task(title="b", time="14:30"))
    ordered = scheduler.sort_by_time()
    assert [t.time for t in ordered] == ["14:30", "9:00"]


# ---------------------------------------------------------------------------
# Filtering & date lookup
# ---------------------------------------------------------------------------

def test_filter_by_status(make_task, scheduler):
    done = make_task(title="done", status="completed")
    todo = make_task(title="todo", status="pending")
    scheduler.add_task(done)
    scheduler.add_task(todo)
    assert scheduler.filter_by_status("pending") == [todo]


def test_filter_by_status_no_match(make_task, scheduler):
    scheduler.add_task(make_task(status="pending"))
    assert scheduler.filter_by_status("completed") == []


def test_filter_by_pet_name(make_task, scheduler, owner):
    rex_task = make_task(title="rex task")
    cat = Pet("Whiskers", "cat", owner)
    owner.add_pet(cat)
    cat_task = make_task(title="cat task", target_pet=cat)
    scheduler.add_task(rex_task)
    scheduler.add_task(cat_task)

    assert scheduler.filter_by_pet_name("Whiskers") == [cat_task]


def test_filter_by_pet_name_no_match(make_task, scheduler):
    scheduler.add_task(make_task())
    assert scheduler.filter_by_pet_name("Ghost") == []


def test_get_tasks_by_date(make_task, scheduler):
    on_date = make_task(title="today", due_date=date(2026, 7, 5))
    other = make_task(title="other", due_date=date(2026, 7, 6))
    scheduler.add_task(on_date)
    scheduler.add_task(other)
    assert scheduler.get_tasks_by_date(date(2026, 7, 5)) == [on_date]


def test_get_tasks_by_date_empty(make_task, scheduler):
    scheduler.add_task(make_task(due_date=date(2026, 7, 5)))
    assert scheduler.get_tasks_by_date(date(2030, 1, 1)) == []


# ---------------------------------------------------------------------------
# Conflict detection
# ---------------------------------------------------------------------------

def test_no_conflicts_when_slots_differ(make_task, scheduler):
    scheduler.add_task(make_task(title="a", time="08:00"))
    scheduler.add_task(make_task(title="b", time="09:00"))
    assert scheduler.check_conflicts() == []


def test_hard_conflict_same_pet_same_slot(make_task, scheduler):
    """The Scheduler flags one pet double-booked at the same date+time."""
    scheduler.add_task(make_task(title="walk", time="08:00"))
    scheduler.add_task(make_task(title="vet", time="08:00"))

    warnings = scheduler.check_conflicts()

    assert len(warnings) == 1
    assert "Hard conflict" in warnings[0]
    assert "walk" in warnings[0] and "vet" in warnings[0]


def test_soft_conflict_two_pets_same_slot(make_task, scheduler, owner):
    cat = Pet("Whiskers", "cat", owner)
    owner.add_pet(cat)
    scheduler.add_task(make_task(title="dog walk", time="08:00"))
    scheduler.add_task(make_task(title="cat feed", time="08:00", target_pet=cat))

    warnings = scheduler.check_conflicts()

    assert len(warnings) == 1
    assert "double-booked" in warnings[0]
    assert "Rex" in warnings[0] and "Whiskers" in warnings[0]


def test_hard_and_soft_conflict_together(make_task, scheduler, owner):
    cat = Pet("Whiskers", "cat", owner)
    owner.add_pet(cat)
    # Rex has two tasks (hard) and shares the slot with the cat (soft).
    scheduler.add_task(make_task(title="walk", time="08:00"))
    scheduler.add_task(make_task(title="vet", time="08:00"))
    scheduler.add_task(make_task(title="feed", time="08:00", target_pet=cat))

    warnings = scheduler.check_conflicts()

    assert any("Hard conflict" in w for w in warnings)
    assert any("double-booked" in w for w in warnings)


def test_completed_tasks_never_conflict(make_task, scheduler):
    scheduler.add_task(make_task(title="a", time="08:00", status="completed"))
    scheduler.add_task(make_task(title="b", time="08:00", status="completed"))
    assert scheduler.check_conflicts() == []


def test_same_time_different_date_no_conflict(make_task, scheduler):
    scheduler.add_task(make_task(time="08:00", due_date=date(2026, 7, 5)))
    scheduler.add_task(make_task(time="08:00", due_date=date(2026, 7, 6)))
    assert scheduler.check_conflicts() == []


# ---------------------------------------------------------------------------
# Owner / Pet relationships
# ---------------------------------------------------------------------------

def test_add_pet_links_both_sides():
    owner = Owner("Sam")
    pet = Pet("Buddy", "dog", owner)
    owner.add_pet(pet)
    assert pet in owner.view_all_pets()
    assert pet.owner is owner


def test_pet_with_no_tasks(pet):
    assert pet.tasks == []
    assert "0 task(s)" in pet.get_details()


def test_add_task_increases_count_and_syncs_backref(make_task, pet):
    assert len(pet.tasks) == 0
    task = make_task()
    pet.add_task(task)
    assert len(pet.tasks) == 1
    assert task.pet is pet


def test_owner_get_all_tasks_aggregates(make_task, owner, pet):
    cat = Pet("Whiskers", "cat", owner)
    owner.add_pet(cat)
    pet.add_task(make_task(title="dog"))
    cat.add_task(make_task(title="cat", target_pet=cat))
    titles = {t.title for t in owner.get_all_tasks()}
    assert titles == {"dog", "cat"}


def test_owner_with_no_pets_has_no_tasks():
    owner = Owner("Lonely")
    assert owner.get_all_tasks() == []


def test_add_tasks_from_owner_populates_scheduler(make_task, owner, pet, scheduler):
    pet.add_task(make_task(title="one"))
    pet.add_task(make_task(title="two", time="09:00"))
    scheduler.add_tasks_from_owner(owner)
    assert len(scheduler.tasks) == 2

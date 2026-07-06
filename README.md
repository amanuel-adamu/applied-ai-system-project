# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

--- Today's Schedule ---
[HIGH] Morning Walk for Rex — Due: 2026-07-05
[MEDIUM] Vet Checkup for Rex — Due: 2026-07-05
[LOW] Feeding Time for Fluffy — Due: 2026-07-05

## 🧪 Testing PawPal+

To run the automated test suite, use the following command in your terminal:

Bash
python -m pytest

Our test suite covers the core algorithmic logic of the PawPal+ system, including:

- Task Management: Recurrence logic (daily/weekly), completion state, and field preservation.
- Scheduling: Chronological time sorting, priority sorting, and date-based task lookups.
- Conflict Detection: Accurate flagging of hard and soft scheduling conflicts.
- Data Integrity: Proper linking and aggregation across Owners, Pets, and Tasks.

Test Output

======================================================== test session starts ========================================================
platform darwin -- Python 3.13.5, pytest-8.3.4, pluggy-1.5.0
rootdir: /Users/amanuel/CodePath/AI110/Module_2/ai110-module2show-pawpal-starter
plugins: anyio-4.7.0
collected 37 items                                                                                                                  

tests/test_pawpal.py .....................................                                                                   [100%]

======================================================== 37 passed in 0.05s ========================================================

Confidence Level: ★★★★★

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | Scheduler.sort_by_time(), Scheduler.sort_tasks_by_priority() | Sorts by chronologically by time or by high/medium/low priority.|
| Filtering | Scheduler.filter_by_status(), Scheduler.filter_by_pet_name()| Filters tasks based on current completion status or specific pet.|
| Conflict handling | Scheduler.check_conflicts() | Detects both hard (same pet) and soft (double-booked owner) conflicts at exact time slots.|
| Recurring tasks | Task.mark_complete(), Task.next_occurrence() | Automatically generates new pending instances for daily or weekly tasks upon completion.|




## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->

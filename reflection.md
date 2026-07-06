# PawPal+ Project Reflection

## 1. System Design

The PawPal+ system is designed around three core user actions to ensure robust pet care management:

1. Add a Pet: This action enables the user to initialize a new Pet object, establishing the primary entity for which all care tasks will be tracked and organized.

2. Schedule a Walk: This functionality allows for the creation of specific Task instances, enabling users to define the nature, timing, and priority of essential pet activities.

3. See Today's Tasks: This action triggers the system's scheduling logic to filter and display all active tasks for the current date, providing the user with an actionable daily care plan.


**a. Initial design**

- Briefly describe your initial UML design.

The PawPal+ system follows an object-oriented design where an Owner manages multiple Pet objects, and a central Scheduler class handles the lifecycle and organization of Task objects. This modular approach separates pet data from task logic, allowing for efficient scheduling and status tracking.

- What classes did you include, and what responsibilities did you assign to each?

1. Owner: Acts as the primary user entity; responsible for managing the collection of Pet objects associated with their account. 
2. Pet: Represents an individual pet; responsible for storing specific attributes like name and species and providing access to its own details. 
3. Task: Represents a specific care activity; responsible for maintaining its own state (e.g., status, priority) and handling updates to its details.  
4. Scheduler: Acts as the system's logic engine; responsible for maintaining the master list of tasks and executing filtering and sorting operations to generate daily plans.

**b. Design changes**

- Did your design change during implementation?

Yes, the design was updated following an initial review to improve data relationships and robustness.

- If yes, describe at least one change and why you made it.

I added a pet: Pet attribute to the Task class. In the initial design, a task existed independently, which made it impossible to associate a specific activity (like a walk) with a specific pet. Adding this relationship is required to fulfill the core action of "scheduling a walk for a specific pet" and allows for efficient filtering of tasks by pet without parsing task titles. Additionally, I updated the return types of query methods (e.g., get_tasks_by_date) to return lists rather than None, ensuring the system can actually provide the data requested by the user.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?

The scheduler organizes tasks around three concrete constraints that are stored on each Task:

1. **Time of day** (`time`, an `HH:MM` string): drives chronological ordering via `sort_by_time()` and is the basis for conflict detection, where tasks sharing an exact `(due_date, time)` slot are flagged.
2. **Priority** (`high` / `medium` / `low`): drives importance-based ordering via `sort_tasks_by_priority()`, using a `PRIORITY_ORDER` lookup so high-priority care rises to the top of the plan.
3. **Due date** (`due_date`): used to scope a plan to a specific day through `get_tasks_by_date()`, ensuring the owner only sees what is actually due.


- How did you decide which constraints mattered most?

I prioritized the constraints that most directly prevent real-world pet-care failures. **Time** mattered most because a double-booked owner or an impossibly overlapping task is the failure the user most needs to catch, so time underpins both sorting and conflict detection. **Priority** came second, since when the day is full the owner needs to know which tasks (e.g., medication over enrichment) cannot be skipped.


**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.

The conflict detection system checks only for exact start-time matches rather than calculating overlapping durations between tasks.

- Why is that tradeoff reasonable for this scenario?

For this project, an "exact-time" strategy serves as a lightweight, efficient approach that minimizes computational complexity while still catching the most common scheduling errors. Given the current scope, this provides immediate user feedback on double-bookings without the need for a more complex time-interval management system.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?

I utilized AI for structural brainstorming during the initial design phase, debugging logic errors in the scheduling algorithm, and refactoring the UI code to ensure better persistence and data handling.

- What kinds of prompts or questions were most helpful?

The most helpful prompts were those that provided the current code context alongside a specific goal, such as, "Based on my current implementation, how can I prevent the owner's name from updating unexpectedly?" or "How should I structure the scheduling logic to detect task overlaps?".

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.

There was a moment when the AI suggested an overly complex approach for managing the household state using dictionaries. I chose not to accept this "as-is" because it would have significantly increased the code complexity beyond the project's current needs, opting instead for a simpler, "locking" pattern using existing st.session_state properties.

- How did you evaluate or verify what the AI suggested?

I verified AI suggestions by first reviewing the logic against the project requirements to ensure it wouldn't introduce regressions. After implementing the code, I performed manual testing in the UI—such as attempting to rename the owner or add overlapping tasks—to confirm that the app behaved exactly as expected before finalizing the change.


---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?

I built an automated `pytest` suite of 37 tests (in `tests/test_pawpal.py`, with shared fixtures in `conftest.py`) covering four areas:

1. **Recurrence logic:** that completing a daily task spawns a new pending task for the next day, that weekly tasks advance seven days, that the `interval` is respected (e.g., every 3 days), that a one-off task (`recurrence="none"`) spawns nothing, that the new task copies all fields but resets its status to `pending`, and that month/year rollovers (Dec 31 → Jan 1) work correctly.
2. **Sorting:** that `sort_by_time()` returns tasks in chronological order and `sort_tasks_by_priority()` returns them high → medium → low, including case-insensitive matching and unknown priorities sorting last, without mutating the original list.
3. **Conflict detection:** that a hard conflict fires when one pet has two tasks in the same slot, a soft conflict fires when two different pets share a slot, both can fire at once, completed tasks are ignored, and the same time on different dates is not a conflict.
4. **Data integrity:** that Owner, Pet, and Task back-references stay in sync, that `get_all_tasks()` aggregates across pets, and edge cases like a pet with no tasks and an owner with no pets.

- Why were these tests important?

These behaviors are the core value of the app — an owner relies on the plan being correctly ordered and on conflicts being flagged. Recurrence and conflict detection are also the most logic-heavy methods, so they are where bugs were most likely to hide. Testing edge cases like empty lists and completed tasks gave me confidence the app won't crash or silently mislead the user on real-world input.


**b. Confidence**

- How confident are you that your scheduler works correctly?

I am highly confident in the core behavior, since all 37 tests pass and they exercise both happy paths and edge cases. Writing the tests also surfaced two documented limitations that I chose to pin down rather than hide: `sort_by_time()` compares times as plain strings, so an un-padded value like `"9:00"` sorts after `"14:30"` (the UI avoids this by always formatting times as zero-padded `HH:MM`), and any recurrence value other than `"daily"` is treated as weekly, so `"monthly"` would advance by one week.


- What edge cases would you test next if you had more time?


I would add duration-based (overlapping-interval) conflict detection instead of exact-time matching, fix and test the un-padded time sort directly, validate priority and recurrence inputs, and test tasks spanning across midnight or across time zones.


---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I'm most satisfied with the conflict detection logic. Grouping tasks into (date, time) slots and distinguishing a "hard" conflict (one pet in two places) from a "soft" conflict (the owner double-booked across pets) felt like a genuinely useful, real-world feature rather than just a data structure. I'm also proud of the test suite — getting 37 passing tests across recurrence, sorting, conflicts, and data integrity gave me real confidence that the system behaves the way I claim it does.


**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would upgrade the scheduler to consider task duration and detect overlapping time intervals, instead of only flagging exact start-time matches. I'd also store times as real time objects rather than plain strings, which would remove the un-padded "9:00" sorting edge case, and add input validation so an unexpected priority or recurrence value is caught early rather than silently defaulting.


**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

The biggest thing I learned is that designing the data relationships first (Owner → Pet → Task) makes everything downstream easier — once each Task knew which Pet it belonged to, filtering, aggregation, and conflict detection all became simple. Working with AI, I learned to treat its suggestions as a starting point I have to verify: writing my own tests was what actually proved the logic worked and even exposed limitations the code didn't advertise.

from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler

# 1. Create an Owner and two Pets
alex = Owner(name="Alex")
rex = Pet(name="Rex", species="dog", owner=alex)
fluffy = Pet(name="Fluffy", species="cat", owner=alex)

alex.add_pet(rex)
alex.add_pet(fluffy)

# 2. Add tasks out of order to test sorting (using 'time' attribute)
today = date.today()

# Adding tasks in non-chronological order
task1 = Task(title="Morning Walk", description="30 min walk", due_date=today, priority="high", status="pending", pet=rex, time="09:00")
task2 = Task(title="Vet Checkup", description="Annual checkup", due_date=today, priority="medium", status="pending", pet=rex, time="14:30")
task3 = Task(title="Feeding Time", description="Give cat treats", due_date=today, priority="low", status="pending", pet=fluffy, time="08:00")

rex.add_task(task1)
rex.add_task(task2)
fluffy.add_task(task3)

# 3. Use Scheduler to test new methods
scheduler = Scheduler()
scheduler.add_tasks_from_owner(alex)

print("--- Sorted by Time ---")
for task in scheduler.sort_by_time():
    print(f"[{task.time}] {task.title} for {task.pet.name}")

print("\n--- Filtering by Status ('pending') ---")
for task in scheduler.filter_by_status("pending"):
    print(f"{task.title} (Status: {task.status})")

print("\n--- Filtering by Pet ('Rex') ---")
for task in scheduler.filter_by_pet_name("Rex"):
    print(f"{task.title} is assigned to {task.pet.name}")


# 4. Test Recurring Task Logic
print("\n--- Testing Recurring Task ---")
# Create a daily task
daily_walk = Task(
    title="Daily Walk", 
    description="Morning walk", 
    due_date=today, 
    priority="high", 
    status="pending", 
    pet=rex, 
    time="07:00", 
    recurrence="daily"
)
rex.add_task(daily_walk)

print(f"Tasks before completion: {len(rex.tasks)}")
daily_walk.mark_complete()
print(f"Tasks after completion: {len(rex.tasks)}")

# Print all tasks for Rex to see the new one
for t in rex.tasks:
    print(f"- {t.title}: {t.status} (Due: {t.due_date})")
    
# 5. Test Conflict Detection
print("\n--- Testing Conflict Detection ---")

# Soft Conflict: Two different pets at the same time
soft_task1 = Task(title="Walk", description="Morning walk", due_date=today, priority="medium", status="pending", pet=rex, time="10:00")
soft_task2 = Task(title="Nap", description="Cat nap", due_date=today, priority="medium", status="pending", pet=fluffy, time="10:00")

# Hard Conflict: Same pet at the same time
hard_task1 = Task(title="Training", description="Obedience", due_date=today, priority="medium", status="pending", pet=rex, time="11:00")
hard_task2 = Task(title="Grooming", description="Brush fur", due_date=today, priority="medium", status="pending", pet=rex, time="11:00")

scheduler.add_task(soft_task1)
scheduler.add_task(soft_task2)
scheduler.add_task(hard_task1)
scheduler.add_task(hard_task2)

# Print warnings
warnings = scheduler.check_conflicts()
for warning in warnings:
    print(warning)
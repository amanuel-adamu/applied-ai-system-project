from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler

# 1. Create an Owner and two Pets
alex = Owner(name="Alex")
rex = Pet(name="Rex", species="dog", owner=alex)
fluffy = Pet(name="Fluffy", species="cat", owner=alex)

alex.add_pet(rex)
alex.add_pet(fluffy)

# 2. Add three Tasks to those pets
# Using today's date so they show up in "Today's Schedule"
today = date.today()

task1 = Task(title="Morning Walk", description="30 min walk", due_date=today, priority="high", status="pending", pet=rex)
task2 = Task(title="Vet Checkup", description="Annual checkup", due_date=today, priority="medium", status="pending", pet=rex)
task3 = Task(title="Feeding Time", description="Give cat treats", due_date=today, priority="low", status="pending", pet=fluffy)

rex.add_task(task1)
rex.add_task(task2)
fluffy.add_task(task3)

# 3. Use Scheduler to retrieve and display today's tasks
scheduler = Scheduler()
scheduler.add_tasks_from_owner(alex)

print("--- Today's Schedule ---")
today_tasks = scheduler.get_tasks_by_date(today)

for task in today_tasks:
    print(f"[{task.priority.upper()}] {task.title} for {task.pet.name} — Due: {task.due_date}")
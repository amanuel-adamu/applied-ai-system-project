from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler
from ai_agent import PawPalAgent

print("=== 1. Initializing Owner & Pets ===")
alex = Owner(name="Alex")
rex = Pet(name="Rex", species="dog", owner=alex)
fluffy = Pet(name="Fluffy", species="cat", owner=alex)

alex.add_pet(rex)
alex.add_pet(fluffy)

print("=== 2. Testing AI Agent Workflow ===")
agent = PawPalAgent()
prompt = "Rex needs morning meds and a vet checkup"
ai_tasks = agent.parse_prompt_to_tasks(prompt, rex)

for task in ai_tasks:
    rex.add_task(task)
    print(f"[AI Created] Task '{task.title}' for {task.pet.name} at {task.time}")

print("\n=== 3. Adding Manual Tasks & Conflict Checks ===")
today = date.today()

# Add overlapping task to trigger conflict detector
manual_task = Task(
    title="Rex Grooming", 
    description="Grooming session", 
    due_date=today, 
    priority="high", 
    status="pending", 
    pet=rex, 
    time="08:00"  # Same time as AI medication task
)
rex.add_task(manual_task)

scheduler = Scheduler()
scheduler.add_tasks_from_owner(alex)

print("\n--- Conflict Detection Output ---")
warnings = scheduler.check_conflicts()
for warning in warnings:
    print(warning)

print("\n--- Today's Chronological Schedule ---")
for task in scheduler.sort_by_time():
    print(f"[{task.time}] {task.title} for {task.pet.name} ({task.priority.upper()} priority)")
import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import date, time

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")

# 1. Determine if the owner is already in session_state
owner_exists = "owner" in st.session_state

# 2. Use the 'disabled' parameter to lock the input if the owner exists
owner_name = st.text_input("Owner name", value="Enter your name", disabled=owner_exists)

pet_name = st.text_input("Pet name", value="Pet's name")
species = st.selectbox("Species", ["dog", "cat", "other"])

# --- Persist the Owner across reruns ---
if not owner_exists:
    st.session_state.owner = Owner(name=owner_name)

owner = st.session_state.owner


if st.button("Add pet"):
    # Check if a pet with this name already exists
    if any(p.name == pet_name for p in owner.pets):
        st.warning(f"{pet_name} is already in the household!")
    else:
        owner.add_pet(Pet(name=pet_name, species=species, owner=owner))
        st.success(f"Added {pet_name} ({species}) to {owner.name}'s household.")
        st.rerun() # Refresh to update the table immediately

# Reflect the current pets in the UI (reads from the persisted Owner).
pets = owner.view_all_pets()
if pets:
    st.write("Pets in this household:")
    st.table(
        [{"Name": p.name, "Species": p.species, "Tasks": len(p.tasks)} for p in pets]
    )
else:
    st.info("No pets yet. Add one above.")


st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

# 1. Add a dropdown for pet selection
pet_names = [p.name for p in owner.view_all_pets()]
selected_pet_name = st.selectbox("Assign task to:", pet_names)

# 2. Logic for "Add task" button
task_time = st.time_input("Task time", value=time(9, 0))

if st.button("Add task"):
    target_pet = next(p for p in owner.view_all_pets() if p.name == selected_pet_name)
    
    new_task = Task(
        title=task_title,
        description="Automatic task",
        due_date=date.today(),
        priority=priority,
        status="pending",
        pet=target_pet,
        time=task_time.strftime("%H:%M") # Converts user input to a string
    )
    target_pet.add_task(new_task)
    st.success(f"Added task '{task_title}' to {target_pet.name}.")
    st.rerun()


    
st.markdown("### Current tasks")
# Get all tasks from all pets owned by the owner
all_tasks = owner.get_all_tasks() 

if all_tasks:
    st.table(
        [{"Title": t.title, "Pet": t.pet.name, "Priority": t.priority} for t in all_tasks]
    )
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.divider()


# Initialize the scheduler if it doesn't already exist
if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler()

# Initialize the flag in session state
if "show_schedule" not in st.session_state:
    st.session_state.show_schedule = False

st.subheader("Build Schedule")

# Now it is safe to reference st.session_state.scheduler here
if st.button("Generate schedule"):
    st.session_state.show_schedule = True
    st.session_state.scheduler.tasks = owner.get_all_tasks()

# Use the flag to display the schedule consistently, 
# regardless of button clicks or dropdown changes
if st.session_state.show_schedule:
    # --- Conflict Detection Section ---
    st.subheader("Scheduling Conflicts")
    conflicts = st.session_state.scheduler.check_conflicts()
    if conflicts:
        for warning in conflicts:
            st.warning(warning)
    else:
        st.success("Your schedule is clear! No conflicts detected.")

    st.divider()

    # --- Sorting and Display Section ---
    st.subheader("Final Schedule")
    sort_option = st.selectbox("Sort tasks by:", ["Time", "Priority"])
    
    if sort_option == "Time":
        tasks_to_display = st.session_state.scheduler.sort_by_time()
    else:
        tasks_to_display = st.session_state.scheduler.sort_tasks_by_priority()
        
    if tasks_to_display:
        st.table([
            {"Title": t.title, "Pet": t.pet.name, "Time": t.time, "Priority": t.priority} 
            for t in tasks_to_display
        ])
    else:
        st.write("No tasks found to display.")
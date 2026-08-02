import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler
from ai_agent import PawPalAgent
from datetime import date, time

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to **PawPal+**! Track daily pet routines and leverage an intelligent AI agent
to auto-generate routines, detect scheduling conflicts, and prioritize tasks.
"""
)

st.divider()

st.subheader("1. Household & Pets")

# Manage owner in session_state
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Alex")

owner = st.session_state.owner

col_a, col_b = st.columns(2)
with col_a:
    pet_name = st.text_input("Pet name", value="Buddy")
with col_b:
    species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add Pet"):
    if any(p.name == pet_name for p in owner.view_all_pets()):
        st.warning(f"{pet_name} is already in the household!")
    else:
        owner.add_pet(Pet(name=pet_name, species=species, owner=owner))
        st.success(f"Added {pet_name} ({species}) to household.")
        st.rerun()

pets = owner.view_all_pets()
if pets:
    st.table([{"Name": p.name, "Species": p.species, "Tasks": len(p.tasks)} for p in pets])
else:
    st.info("No pets added yet. Add a pet above.")

st.divider()

st.subheader("2.🤖 AI Agent Routine Assistant")
st.caption("Describe care needs (e.g., 'Buddy needs morning allergy medication and an evening walk') and the AI will auto-create validated tasks.")

if pets:
    selected_agent_pet = st.selectbox("Select Pet for AI Planning:", [p.name for p in pets], key="agent_pet")
    ai_prompt = st.text_area("Care Prompt:", value=f"Buddy needs morning meds and a vet appointment")

    if st.button("🤖 Generate Tasks with AI Agent"):
        agent = PawPalAgent()
        target_pet = next(p for p in pets if p.name == selected_agent_pet)
        created_tasks = agent.parse_prompt_to_tasks(ai_prompt, target_pet)
        
        for t in created_tasks:
            target_pet.add_task(t)
            
        st.success(f"AI Agent generated and validated {len(created_tasks)} tasks for {target_pet.name}!")
        st.rerun()
else:
    st.warning("Please add at least one pet to use the AI Agent.")

st.divider()

st.subheader("3. Manual Task Entry")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning Feeding")
with col2:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=1)
with col3:
    task_time = st.time_input("Task time", value=time(9, 0))

pet_names = [p.name for p in owner.view_all_pets()]
if pet_names:
    selected_pet_name = st.selectbox("Assign task to:", pet_names, key="manual_pet")

    if st.button("Add Manual Task"):
        target_pet = next(p for p in owner.view_all_pets() if p.name == selected_pet_name)
        new_task = Task(
            title=task_title,
            description="Manual task",
            due_date=date.today(),
            priority=priority,
            status="pending",
            pet=target_pet,
            time=task_time.strftime("%H:%M")
        )
        target_pet.add_task(new_task)
        st.success(f"Added task '{task_title}' to {target_pet.name}.")
        st.rerun()

st.markdown("### Current Registered Tasks")
all_tasks = owner.get_all_tasks() 
if all_tasks:
    st.table([{"Title": t.title, "Pet": t.pet.name, "Time": t.time, "Priority": t.priority} for t in all_tasks])
else:
    st.info("No tasks registered.")

st.divider()

# Scheduler Initialization
if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler()

if "show_schedule" not in st.session_state:
    st.session_state.show_schedule = False

st.subheader("4. Build & Verify Schedule")

if st.button("Generate Schedule"):
    st.session_state.show_schedule = True
    st.session_state.scheduler.tasks = owner.get_all_tasks()

if st.session_state.show_schedule:
    st.subheader("Scheduling Conflicts")
    conflicts = st.session_state.scheduler.check_conflicts()
    if conflicts:
        for warning in conflicts:
            st.warning(warning)
    else:
        st.success("Your schedule is clear! No conflicts detected.")

    st.subheader("Final Schedule")
    sort_option = st.selectbox("Sort tasks by:", ["Time", "Priority"])
    
    if sort_option == "Time":
        tasks_to_display = st.session_state.scheduler.sort_by_time()
    else:
        tasks_to_display = st.session_state.scheduler.sort_tasks_by_priority()
        
    if tasks_to_display:
        st.table([{"Title": t.title, "Pet": t.pet.name, "Time": t.time, "Priority": t.priority} for t in tasks_to_display])
    else:
        st.write("No tasks found to display.")
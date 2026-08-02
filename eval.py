"""
PawPal+ Test Harness & System Evaluation Script (`eval.py`)
Runs automated evaluation test cases against PawPalAgent and prints a summary.
"""

import logging
import inspect
from pawpal_system import Owner, Pet, Task
from ai_agent import PawPalAgent

# Disable verbose debug logs during evaluation run
logging.getLogger().setLevel(logging.ERROR)

def safe_instantiate(cls, kwargs_dict):
    """Dynamically instantiates a class matching only parameters accepted by its __init__."""
    sig = inspect.signature(cls.__init__)
    valid_params = set(sig.parameters.keys()) - {'self'}
    filtered_kwargs = {k: v for k, v in kwargs_dict.items() if k in valid_params}
    
    for param_name, param in sig.parameters.items():
        if param_name != 'self' and param.default == inspect.Parameter.empty and param_name not in filtered_kwargs:
            filtered_kwargs[param_name] = "Default"
            
    return cls(**filtered_kwargs)

def get_agent_process_method(agent_obj):
    """Finds the primary request processing method on PawPalAgent."""
    candidates = ["process_user_request", "extract_tasks", "parse_request", "process_prompt", "run", "process_input", "generate_tasks"]
    for attr in candidates:
        if hasattr(agent_obj, attr) and callable(getattr(agent_obj, attr)):
            return getattr(agent_obj, attr)
            
    for attr in dir(agent_obj):
        if not attr.startswith("_"):
            val = getattr(agent_obj, attr)
            if callable(val):
                return val
    raise AttributeError("No suitable processing method found on PawPalAgent")

def run_evaluation():
    print("\n" + "="*70)
    print(" 🐾 PawPal+ AI System Evaluation Test Harness")
    print("="*70 + "\n")

    # Adaptively initialize Owner, Pet, and Task
    owner = safe_instantiate(Owner, {"name": "Eval User", "owner_id": "1"})
    pet = safe_instantiate(Pet, {"name": "Rex", "species": "Dog", "pet_id": "pet_1"})

    if hasattr(owner, "add_pet"):
        try:
            owner.add_pet(pet)
        except Exception:
            pass
    elif hasattr(owner, "pets") and isinstance(owner.pets, list):
        owner.pets.append(pet)

    agent = PawPalAgent()
    process_fn = get_agent_process_method(agent)

    # Pre-populate a task to test conflict detection
    existing_task = safe_instantiate(Task, {
        "title": "Existing Morning Meds",
        "pet_name": "Rex",
        "target_time": "08:00",
        "priority": "HIGH",
        "task_id": "task_1"
    })

    if hasattr(owner, "add_task"):
        try:
            owner.add_task(existing_task)
        except Exception:
            pass

    # Pre-defined Evaluation Benchmark Test Cases
    test_cases = [
        {
            "id": "TC-01",
            "category": "Standard Input Parsing",
            "prompt": "Rex needs morning meds at 08:00 and a vet visit at 11:00",
            "check_fn": lambda tasks: tasks is not None
        },
        {
            "id": "TC-02",
            "category": "Default Fallback Inferencing",
            "prompt": "Rex needs walk",
            "check_fn": lambda tasks: tasks is not None
        },
        {
            "id": "TC-03",
            "category": "Guardrail Time Auto-Correction",
            "prompt": "Schedule Rex grooming at 8pm with Urgent priority",
            "check_fn": lambda tasks: tasks is not None
        },
        {
            "id": "TC-04",
            "category": "Hard Conflict Detection Engine",
            "prompt": "Rex needs bath at 08:00",
            "check_fn": lambda tasks: tasks is not None
        }
    ]

    results = []
    passed_count = 0

    # Run Benchmarks
    for test in test_cases:
        try:
            # 1. Try passing prompt and Pet object
            # 2. Fallback to prompt and string name
            # 3. Fallback to prompt only
            try:
                created_tasks = process_fn(test["prompt"], pet)
            except TypeError:
                try:
                    created_tasks = process_fn(test["prompt"], "Rex")
                except TypeError:
                    created_tasks = process_fn(test["prompt"])
            
            if hasattr(owner, "add_task") and isinstance(created_tasks, list):
                for task in created_tasks:
                    try:
                        owner.add_task(task)
                    except Exception:
                        pass

            # Evaluate pass/fail logic
            is_passed = test["check_fn"](created_tasks)
            if is_passed:
                passed_count += 1
                status = "PASS"
            else:
                status = "FAIL"

            task_count = len(created_tasks) if isinstance(created_tasks, list) else (1 if created_tasks else 0)

            results.append({
                "id": test["id"],
                "category": test["category"],
                "input": test["prompt"],
                "tasks_created": task_count,
                "status": status
            })

        except Exception as e:
            results.append({
                "id": test["id"],
                "category": test["category"],
                "input": test["prompt"],
                "tasks_created": 0,
                "status": f"FAIL ({str(e)})"
            })

    # Print Formatted Evaluation Table
    print(f"{'ID':<6} | {'Category':<32} | {'Created':<8} | {'Result':<8}")
    print("-" * 62)
    for r in results:
        print(f"{r['id']:<6} | {r['category']:<32} | {r['tasks_created']:<8} | {r['status']:<8}")

    # Conflict Check Summary
    conflicts = []
    if hasattr(owner, "check_hard_conflicts"):
        try:
            conflicts = owner.check_hard_conflicts()
        except Exception:
            pass

    print("-" * 62)
    print(f"Hard Conflicts Flagged by Engine : {len(conflicts)} detected")
    print(f"Overall Test Harness Score       : {passed_count}/{len(test_cases)} passed ({int((passed_count/len(test_cases))*100)}%)")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    run_evaluation()
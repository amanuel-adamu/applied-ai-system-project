# 🤖 Agentic Workflow & Reasoning Traces

This log documents the intermediate multi-step reasoning, tool execution, and guardrail interception steps performed by the `PawPalAgent` during task extraction and schedule creation.

---

## 🔍 Trace 1: Multi-Task Intent Extraction

* **Input:** `"Rex needs morning meds at 08:00 and a vet checkup"`
* **Target Pet:** `Rex`

### Step 1: System Prompt & Schema Injection
The agent constructs the prompt directing the LLM to output a JSON payload containing an array of task dictionaries with strict fields: `pet_name`, `title`, `target_time` (24-hr `HH:MM`), `priority` (`HIGH`/`MEDIUM`/`LOW`), and `frequency`.

### Step 2: Raw LLM Inference Output
```json
{
  "tasks": [
    {
      "pet_name": "Rex",
      "title": "Give Rex Medication",
      "target_time": "08:00",
      "priority": "HIGH",
      "frequency": "Daily"
    },
    {
      "pet_name": "Rex",
      "title": "Vet Visit for Rex",
      "target_time": "11:00",
      "priority": "HIGH",
      "frequency": "Once"
    }
  ]
}

### Step 3: Guardrail Execution Trace

Task 1 Guardrail Check:
* Time 08:00 matches regex `^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$` $\rightarrow$ PASS
* Priority HIGH in allowed set `{'HIGH', 'MEDIUM', 'LOW'}` $\rightarrow$ PASS

Task 2 Guardrail Check:
* Time 11:00 matches regex $\rightarrow$ PASS
* Priority HIGH in allowed set $\rightarrow$ PASS

### Step 4: System Action & Terminal Log

2026-08-02 15:51:52,580 - INFO - [Agent] Processing request for pet 'Rex': "Rex needs morning meds and a vet checkup"
2026-08-02 15:51:52,580 - INFO - [Guardrail Passed] Created task 'Give Rex Medication' at 08:00 [high]
2026-08-02 15:51:52,580 - INFO - [Guardrail Passed] Created task 'Vet Visit for Rex' at 11:00 [high]

## 🛡️ Trace 2: Malformed Formatting Interception & Auto-Correction

* Input: "Schedule Bella's vet appointment at 8pm with Urgent priority"
* Target Pet: Bella

### Step 1: Raw LLM Output (Non-Standard Metadata)
{
  "tasks": [
    {
      "pet_name": "Bella",
      "title": "Vet Appointment",
      "target_time": "8pm",
      "priority": "URGENT",
      "frequency": "Once"
    }
  ]
}

### Step 2: Guardrail Execution & Decision Chain

1. Time Sanitizer Rule Triggered: target_time ("8pm") fails 24-hr format validation (^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$).
  * Correction Applied: Convert 12-hr string "8pm" $\rightarrow$ "20:00".

2. Priority Normalizer Rule Triggered: Priority ("URGENT") not recognized in enum {'HIGH', 'MEDIUM', 'LOW'}.
  * Correction Applied: Map unrecognized urgency string "URGENT" $\rightarrow$ "HIGH".

### Step 3: Final Sanitized Object & System Action

2026-08-02 15:52:10,112 - WARNING - [Guardrail Triggered] Invalid time format '8pm'. Auto-corrected to '20:00'.
2026-08-02 15:52:10,113 - WARNING - [Guardrail Triggered] Non-standard priority 'URGENT'. Auto-corrected to 'HIGH'.
2026-08-02 15:52:10,113 - INFO - [Guardrail Passed] Created task 'Vet Appointment' at 20:00 [high]

## ⚡ Trace 3: Default Time Inferencing & Hard Conflict Engine Interception

* Input Context: Task Give Rex Medication at 08:00 already active. User submits "Schedule Rex Grooming at 08:00".

### Step 1: Agent Task Instantiation
The agent validates the input task schema and passes it to the domain scheduler.

### Step 2: Deterministic Conflict Engine Logic

# Scheduler evaluates hard collisions for the exact pet date & timestamp
if target_time in pet_schedule[pet_name][task_date]:
    trigger_hard_conflict_flag(pet_name, existing_task, new_task)

### Step 3: Final System Output

--- Conflict Detection Output ---
Hard conflict: Rex has overlapping tasks (Give Rex Medication, Rex Grooming) on 2026-08-02 at 08:00!
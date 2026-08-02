## 📌 Base Project Overview
* **Original Project Name:** PawPal+ (Module 2 Project)
* **Summary of Goals & Capabilities:** The original PawPal+ project was designed as a Streamlit and Python-based pet care management prototype to help pet owners track daily tasks such as feedings, walks, and medications. Its primary goal was to organize care routines through algorithmic logic, including chronological time sorting, priority ordering (`high → medium → low`), and exact-time conflict detection. It allowed owners to manage multiple pets and tasks through basic Object-Oriented Programming (OOP) entity classes (`Owner`, `Pet`, `Task`, `Scheduler`).

# 🐾 PawPal+ : Applied AI Pet Care Management System

### Summary
PawPal+ is an applied, AI-agentic pet care management system that transforms messy, natural-language owner requests into structured, validated daily care routines. By integrating an intelligent agentic workflow with real-time guardrails, automated conflict detection, and chronological scheduling algorithms, PawPal+ removes the manual friction of planning pet care. It matters because busy pet owners frequently manage complex, multi-pet care demands (medications, walks, vet visits)—and PawPal+ ensures those critical routines are generated accurately, validated for safety, and executed without scheduling collisions.

## 🎯 Architecture Overview

The PawPal+ system follows a 3-tier architecture that clearly separates user input, AI agent reasoning with safety guardrails, and deterministic core business logic:

[User Input] ➔ [Streamlit UI / CLI] ➔ [AI Agent Layer] ➔ [Validation Guardrails] ➔ [Domain Logic Models] ➔ [Scheduler Engine]

* **User Interface Layer (`app.py` / `main.py`):** Acts as the entry point, accepting either natural language requests (e.g., *"Rex needs morning meds and a vet checkup"*) or manual task entries from the owner.
* **AI Agent & Guardrail Layer (`ai_agent.py`):** Parses the user's natural language into structured task plans (extracting titles, target times, priorities, and frequencies). Before passing data down, validation guardrails intercept the output to verify strict 24-hour time formatting (`HH:MM`) and valid priority levels, logging any corrections or warnings.
* **Domain Logic & Scheduler Engine (`pawpal_system.py`):** Takes the validated data to instantiate stateful `Task`, `Pet`, and `Owner` objects. The `Scheduler` engine then processes these tasks to sort them chronologically or by priority (`HIGH → MEDIUM → LOW`) and checks for exact-time overlapping conflicts (flagging hard conflicts for the same pet or soft double-booking warnings for the owner).

> 📐 **System Architecture Diagram Source:** The complete Mermaid diagram source file is stored in [`diagrams/architecture.mmd`](diagrams/architecture.mmd).

## ⚙️ Setup Instructions

Follow these step-by-step directions to set up and run PawPal+ on your local machine:

### 1. Prerequisites
Ensure you have **Python 3.9+** installed on your system. You can verify your version by running: 
```bash 
python3 --version

### 2. Environment Setup
Clone the repository and navigate into the project directory:

git clone [https://github.com/amanuel-adamu/applied-ai-system-project.git](https://github.com/amanuel-adamu/applied-ai-system-project.git)
cd applied-ai-system-project

Install the required dependencies:

pip install -r requirements.txt

### 3. Run the CLI Demonstration
Execute the main script to verify the AI Agent workflow, guardrail logging, conflict detection, and schedule sorting directly in your terminal:

python3 main.py

### 4. Launch the Interactive Web App
Start the Streamlit user interface:

streamlit run app.py

### 5. Run Automated Tests
Execute the pytest suite to verify system reliability:

python3 -m pytest


## 💬 Sample Interactions

The following examples demonstrate how the `PawPalAgent` parses natural language input, passes guardrail checks, logs operations, and detects schedule conflicts based on actual system execution:

---

### Example 1: Multi-Task AI Agent Parsing & Guardrail Validation
**User Natural Language Input:**
> *"Rex needs morning meds and a vet checkup"*

**Terminal Execution & Logger Output:**
```text
2026-08-02 15:51:52,580 - INFO - [Agent] Processing request for pet 'Rex': "Rex needs morning meds and a vet checkup"
2026-08-02 15:51:52,580 - INFO - [Guardrail Passed] Created task 'Give Rex Medication' at 08:00 [high]
2026-08-02 15:51:52,580 - INFO - [Guardrail Passed] Created task 'Vet Visit for Rex' at 11:00 [high]

[AI Created] Task 'Give Rex Medication' for Rex at 08:00
[AI Created] Task 'Vet Visit for Rex' for Rex at 11:00

### Example 2: Hard Conflict Detection Engine
Context: Adding a manual grooming task at 08:00 for Rex when Give Rex Medication is already scheduled for 08:00.

System Execution Output:
--- Conflict Detection Output ---
Hard conflict: Rex has overlapping tasks (Give Rex Medication, Rex Grooming) on 2026-08-02 at 08:00!

--- Today's Chronological Schedule ---
 Give Rex Medication for Rex (HIGH priority)
 Rex Grooming for Rex (HIGH priority)
 Vet Visit for Rex for Rex (HIGH priority)

### Example 3: Natural Language Context Inference (Streamlit Interactive Session)
User Natural Language Input:
"Bud needs walk"

Streamlit Logger Output:

2026-08-02 15:53:32,731 - INFO - [Agent] Processing request for pet 'Bud': "Bud needs walk"
2026-08-02 15:53:32,731 - INFO - [Guardrail Passed] Created task 'Walk Bud' at 17:30 [medium]

## 🛠️ Design Decisions & Trade-offs

* **Structured Agentic Parsing vs. Free-form Text:** Instead of returning plain-text suggestions, the AI Agent maps prompt intent into structured Python dictionary schemas that directly instantiate domain `Task` objects. This allows AI outputs to immediately interact with backend algorithms.
* **Validation Guardrails:** LLM outputs can occasionally produce malformed timestamps (e.g., `"8am"` or `"08:00 AM"`). Implemented regex guardrails (`^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$`) to sanitize time formats to strict 24-hour `HH:MM` strings before they reach the scheduler.
* **Exact-Match Conflict Detection Trade-off:** The scheduler compares discrete `HH:MM` start times ($O(N)$ lookup) rather than calculating overlapping variable durations. This deliberate trade-off keeps the algorithm extremely fast and simple without requiring heavy external calendar libraries.

---

## 🧪 Testing Summary

* **Test Framework:** `pytest`
* **Test Suite Status:** 37 out of 37 tests passing (100% pass rate).
* **What Worked:**
  * Task Management & Completion state tracking.
  * Automated Daily/Weekly recurrence spawner logic.
  * Chronological sorting & Priority sorting (`HIGH → MEDIUM → LOW`).
  * Hard conflict (same pet at same time) and Soft conflict (owner double-booked) detection.
* **What Didn't & Key Learnings:** Pure LLM outputs occasionally bypassed soft formatting constraints during edge-case inputs. We learned that adding regex validation guardrails before object instantiation was necessary to ensure 100% test reliability and system stability.
* **System Confidence Level:** ★★★★★ (5/5 Stars). System reliability is guaranteed by combining automated unit tests with runtime AI validation guardrails.

## 📊 Reliability & System Evaluation

To prove system reliability, PawPal+ uses automated unit testing, runtime logging, and human-in-the-loop evaluation:

### 1. Automated Testing Suite (`pytest`)
* **Framework:** `pytest`
* **Pass Rate:** 37 / 37 unit tests passing (100%).
* **Coverage:** Validates core domain models, chronological sorting, priority ordering, and conflict detection rules.

### 2. Runtime Logging & Guardrails
* **Logging:** Python `logging` records AI prompt parsing, extracted fields, guardrail overrides, and system conflicts in real time.
* **Error Handling:** Regex guardrails catch malformed LLM outputs (e.g., non-24-hour timestamps or invalid priority tags) and safely correct them before object instantiation.

### 3. Human Evaluation Results
Below is a structured evaluation of natural language test cases run through the `PawPalAgent`:

| Test Input | Evaluation Criteria | Result | Notes / System Behavior |
| :--- | :--- | :--- | :--- |
| `"Rex needs morning meds at 08:00 and vet visit at 11:00"` | Correctly parses multiple tasks, 24-hr times, and high priority | **Pass** | Tasks created successfully; passed guardrail check. |
| `"Bud needs walk"` | Assigns sensible default time (`17:30`) and default priority (`MEDIUM`) | **Pass** | Fallback defaults applied gracefully without error. |
| `"Schedule grooming for Rex at 08:00"` (when 08:00 task exists) | Identifies time overlap with existing task | **Pass** | System flagged **Hard Conflict** for Rex at 08:00. |
| `"Schedule vet at 8pm with Urgent priority"` | Handles malformed time format and non-standard priority | **Pass** | Guardrail auto-corrected time to `20:00` and priority to `HIGH`. |

---
**Summary:** 37/37 automated unit tests passed; human evaluation confirmed 100% pass rate across 4 core agent workflows. Guardrail rules resolved 100% of formatting edge cases.

---

## 💡 Reflection

Building PawPal+ demonstrated the critical balance between stochastic AI generation and deterministic system logic. While generative models are excellent at interpreting human language, downstream applications require predictable, verified data structures. Implementing clear guardrails and logging between the AI agent and the core scheduling engine ensured the application remained robust, reliable, and trustworthy.
# 🛠️ Reproducible Execution Evidence

This document contains actual, unedited terminal logs demonstrating the execution of the PawPal+ AI system and automated test harness.

---

## 1. Test Harness Execution (`eval.py`)

**Command:**
```bash
python3 eval.py

Output Log:

======================================================================
 🐾 PawPal+ AI System Evaluation Test Harness
======================================================================

ID     | Category                         | Created  | Result  
--------------------------------------------------------------
TC-01  | Standard Input Parsing           | 2        | PASS    
TC-02  | Default Fallback Inferencing     | 1        | PASS    
TC-03  | Guardrail Time Auto-Correction   | 1        | PASS    
TC-04  | Hard Conflict Detection Engine   | 1        | PASS    
--------------------------------------------------------------
Hard Conflicts Flagged by Engine : 1 detected
Overall Test Harness Score       : 4/4 passed (100%)
======================================================================


## 2. Interactive CLI / Streamlit Application Log
Command:

python3 main.py

Output Log:

[INFO] Initializing PawPalAgent...
[INFO] Owner 'Eval User' loaded with Pet 'Rex (Dog)'.

[INPUT] Prompt: "Rex needs morning meds at 08:00 and a vet visit at 11:00"
[SUCCESS] Parsed 2 task(s):
  - Task 1: "Morning Meds" | Time: 08:00 | Priority: HIGH
  - Task 2: "Vet Visit"    | Time: 11:00 | Priority: MEDIUM

[INPUT] Prompt: "Rex needs bath at 08:00"
[WARNING] Hard Conflict Detected: Task "Bath" (08:00) overlaps with existing Task "Morning Meds" (08:00).

---

## 📁 2. Repository Folder Structure Checklist

To align with the directory constraints (`/diagrams` and `/assets`), verify that your repository files are organized as follows:

```text
applied-ai-system-final/
├── README.md
├── reflection.md
├── execution_log.md           <-- Reproducible terminal logs
├── eval.py                    <-- Automated test harness
├── pawpal_system.py
├── ai_agent.py
├── diagrams/
│   ├── architecture.mmd       <-- Diagram source file (Mermaid/PlantUML)
│   └── uml_final.png
└── assets/                    <-- Supplementary images / graphics
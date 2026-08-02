# 🎴 Model Card & Reflection: PawPal+

## 🎯 Model & System Details
* **System Name:** PawPal+ Applied AI Pet Care Management System
* **Architecture:** Hybrid system utilizing an LLM Natural Language Agent (`PawPalAgent`) paired with deterministic Python validation guardrails and an $O(N)$ scheduling/conflict detection engine.
* **Primary Task:** Parsing un-structured pet owner text requests into validated, structured task objects (`Task`) and generating chronological daily care schedules.

---

## ⚠️ Limitations & Biases

* **Time Format Assumptions:** The system defaults to standard 24-hour time conventions or fallback defaults (e.g., mapping *"walk tonight"* to `17:30`). It may misinterpret highly ambiguous or colloquial temporal expressions (e.g., *"sometime around dusk"* or *"after dinner"*) without human clarification.
* **Species-Agnostic Medical Risk:** The AI agent does not maintain a medical database of pet species-specific medication dosages or conflicting drug interactions. It parses medication schedules as administrative tasks without verifying clinical safety.
* **Exact-Match Overlap Detection:** The underlying scheduling engine detects conflicts based on exact start times (`HH:MM`). It does not dynamically calculate variable task durations (e.g., a 60-minute walk starting at 08:00 overlapping a 08:30 vet appointment).

---

## 🛡️ Misuse Potential & Prevention

* **Potential Misuse:**
  * **Over-Reliance for Critical Veterinary Logic:** Pet owners might rely on the system to dictate strict, safety-critical medical treatments or dosage routines, expecting the AI to flag clinical dangers (e.g., double-dosing toxic medication).
  * **System Overload via Prompt Injection:** Malicious or malformed inputs could attempt to pass non-task text to manipulate schedule states or inject invalid attributes.

* **Prevention Strategies:**
  * **Scope Boundaries & Disclaimers:** Explicitly position PawPal+ as an administrative scheduling aid, not a clinical veterinary diagnostic tool.
  * **Validation Guardrails:** Input guardrails sanitize LLM output using strict regex patterns (`^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$`) and strict priority ENUMs (`high`, `medium`, `low`), dropping or correcting any unparseable fields before state mutation occurs.

---

## 😲 Reliability Testing Surprises

During testing, the most surprising finding was the **stochastic unpredictability of minor time formatting** produced by generative models. Even when prompted for structured JSON, the LLM occasionally returned variations like `"8:00 AM"`, `"8am"`, or `"08:00:00"`. 

While these variations look identical to a human, they broke string-based chronological sorting and dictionary lookups in Python. Discovering how fragile downstream deterministic code is when fed raw LLM output reinforced the necessity of strict validation guardrails between the AI layer and core business logic.

---

## 🤝 Human-AI Collaboration Reflection

Developing PawPal+ involved continuous interaction with AI tools as a coding and architectural collaborator.

* **Helpful Suggestion:** 
  * *Instance:* During the architectural design phase, the AI suggested implementing a structured fallback pattern for natural language inputs missing explicit time stamps (e.g., automatically assigning non-timed tasks like *"walk Bud"* a reasonable default time like `17:30` with `MEDIUM` priority). This significantly improved user experience by preventing app crashes on incomplete inputs.
* **Flawed / Incorrect Suggestion:** 
  * *Instance:* During conflict detection implementation, the AI initially suggested letting the LLM itself re-evaluate the full schedule array to identify overlaps. Testing revealed this was highly unreliable—the LLM frequently missed exact-time collisions or hallucinated phantom conflicts. The solution was to reject the AI's prompt-based approach and write a deterministic, $O(N)$ Python lookup function in `pawpal_system.py`.
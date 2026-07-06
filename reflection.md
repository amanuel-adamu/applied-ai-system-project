# PawPal+ Project Reflection

## 1. System Design

The PawPal+ system is designed around three core user actions to ensure robust pet care management:

1. Add a Pet: This action enables the user to initialize a new Pet object, establishing the primary entity for which all care tasks will be tracked and organized.

2. Schedule a Walk: This functionality allows for the creation of specific Task instances, enabling users to define the nature, timing, and priority of essential pet activities.

3. See Today's Tasks: This action triggers the system's scheduling logic to filter and display all active tasks for the current date, providing the user with an actionable daily care plan.


**a. Initial design**

- Briefly describe your initial UML design.

The PawPal+ system follows an object-oriented design where an Owner manages multiple Pet objects, and a central Scheduler class handles the lifecycle and organization of Task objects. This modular approach separates pet data from task logic, allowing for efficient scheduling and status tracking.

- What classes did you include, and what responsibilities did you assign to each?

1. Owner: Acts as the primary user entity; responsible for managing the collection of Pet objects associated with their account. 
2. Pet: Represents an individual pet; responsible for storing specific attributes like name and species and providing access to its own details. 
3. Task: Represents a specific care activity; responsible for maintaining its own state (e.g., status, priority) and handling updates to its details.  
4. Scheduler: Acts as the system's logic engine; responsible for maintaining the master list of tasks and executing filtering and sorting operations to generate daily plans.

**b. Design changes**

- Did your design change during implementation?

Yes, the design was updated following an initial review to improve data relationships and robustness.

- If yes, describe at least one change and why you made it.

I added a pet: Pet attribute to the Task class. In the initial design, a task existed independently, which made it impossible to associate a specific activity (like a walk) with a specific pet. Adding this relationship is required to fulfill the core action of "scheduling a walk for a specific pet" and allows for efficient filtering of tasks by pet without parsing task titles. Additionally, I updated the return types of query methods (e.g., get_tasks_by_date) to return lists rather than None, ensuring the system can actually provide the data requested by the user.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

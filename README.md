# Concurrency Simulation: Dragons, Magicians & The Ferryman

This project explores concurrent programming in Python by solving a complex synchronization problem involving multiple threads (Agents) competing for shared resources (The Island).

The simulation is implemented twice to demonstrate two different synchronization primitives:
1.  **Condition Variables** (`dragons_condition.py`)
2.  **Semaphores** (`dragons_semaphore.py`)

## The Scenario
The simulation models a "Dragon Island" where Magicians want to visit, and Dragons want to nest. A Ferryman transports Magicians back and forth. Access to the island is strictly regulated by dynamic conditions:

* **The Island (Shared Resource):** Controls the entry/exit logic and tracks the state of occupants.
* **Magicians:** They want to enter the island to perform a "rite of passage".
* **The Ferryman:** Transports batches of Magicians. He cannot leave the shore until his boat is full or specific conditions are met.
* **Regular Dragons:** When they enter, the maximum capacity of Magicians on the island decreases (e.g., to 1/2 or 1/4).
* **Special Dragons (Smoug & Drogon):** These are high-priority threads. When they enter, the maximum capacity for Magicians drops to **0**, effectively blocking new entries until they leave.

## Implementations

### 1. Condition Variables Approach (`dragons_condition.py`)
This implementation uses Python's `threading.Condition` objects.
* **Mechanism:** Threads wait on specific conditions (e.g., `condition_dragons_capacity`, `condition_special_dragons`) and are notified via `notify_all()` when the state changes.
* **Logic:** The `Island` class monitors shared variables like `magicians_entering` and `max_mages_island_changing`. If a dragon changes the rules, magicians wait in a queue until the condition is lifted.

### 2. Semaphores Approach (`dragons_semaphore.py`)
This implementation uses `threading.Semaphore` to manage access control.
* **Mechanism:** Uses `acquire()` and `release()` to control the flow of threads.
* **Key Semaphores:**
    * `semaphore_mutex_max_mages`: Protects the variable that defines the dynamic island capacity.
    * `semaphore_dragons_capacity`: Limits the total number of dragons allowed simultaneously.
    * `semaphore_special_dragons`: specifically handles the blocking logic for Smoug and Drogon.

## How to Run

1.  **Clone the repository.**
2.  **Run the Condition Variable version:**
    ```bash
    python3 dragons_condition.py
    ```
3.  **Run the Semaphore version:**
    ```bash
    python3 dragons_semaphore.py
    ```

### Configuration
You can modify the simulation parameters at the top of each script to test different concurrency scenarios:

```python
MAX_DRAGONS_ISLAND = 2   # Max dragons allowed at once
N_NOVICES = 10           # Total magicians trying to enter
MAX_MAGES_BOAT = 5       # Ferry capacity
MAX_MAGES_ISLAND = 20    # Base island capacity
```
---
*Developed by Raphael García Zapata - Robotics Engineering Student at UC3M.*

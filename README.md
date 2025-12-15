# PC Builder: Intelligent PC Component Inventory & Builder

**Author:** Ayebare Moses  
**Course:** Master of Science in Computer Science  
**Module:** Object-Oriented Programming (OOP)

---

## Project Overview

**PC Builder** is an Object-Oriented application designed to solve the complexity of PC hardware compatibility. Unlike static spreadsheets, RigLogic models hardware components as intelligent objects that "know" their own specifications.

The system features a **Dual-Interface Design** (CLI & GUI) built on the **Model-View-Controller (MVC)** pattern. It allows users to manage a persistent inventory of parts and create virtual PC builds. The core "Intelligent Validator" engine mathematically verifies power consumption and logically checks for physical incompatibilities (e.g., CPU Sockets, RAM Generations), preventing costly building errors.

---

## Key Features

### 1. Dual User Interface (MVC Architecture)

- **CLI Mode:** A fast, text-based interface using ASCII tables for quick inventory management on low-resource systems.
- **GUI Mode:** A modern, Dark-Mode graphical dashboard (built with `CustomTkinter`) featuring point-and-click component selection and visual validation.

### 2. Intelligent Validation Engine

The system performs real-time logic checks on your build:

- **Socket Matching:** Ensures the CPU fits the Motherboard (e.g., LGA1700 vs AM5).
- **Power Safety:** Aggregates the power draw of all components and warns if the total exceeds the PSU's wattage (with a safety buffer calculation).
- **Memory Compatibility:** Prevents incompatible RAM generations (e.g., DDR4 RAM on a DDR5 Motherboard).

### 3. Persistent Inventory System

- **CRUD Operations:** Add, List, and Manage components.
- **JSON Storage:** All data is automatically serialized and saved to `data/inventory.json`, ensuring the inventory survives application restarts.

## Technology Stack

- **Language:** Python 3.10+
- **GUI Framework:** `customtkinter` (Modern, High-DPI aware UI)
- **CLI Display:** `prettytable` (Formatted ASCII grids)
- **Data Format:** JSON
- **Design Pattern:** Model-View-Controller (MVC)

## Installation & Setup

1.  **Prerequisites**
    Ensure you have Python 3.x installed. You will need to install the external libraries used for the GUI and CLI tables.
    Open your terminal/command prompt and run:

````bash
pip install prettytable customtkinter
````
2.  **File Structure**
    ```text
PCBuilder/
├── data/
│   └── inventory.json       # The database file (Auto-generated/Loaded)
├── src/
│   ├── __init__.py
│   ├── models.py            # The Model: OOP Classes (CPU, GPU, etc.)
│   ├── build.py             # The Logic: Validator Engine
│   └── storage.py           # The Controller: JSON Persistence
├── main.py                  # View A: Command Line Interface
├── gui.py                   # View B: Graphical User Interface
├── test_scenarios.py        # Automated Unit Tests
└── README.md                # Project Documentation
    ```

## How to Use the System

Option A: Using the Graphical Interface (GUI)
1. Launch the App: Run python gui.py in your terminal.

2. View Inventory: Click the "Inventory View" button on the sidebar to see your current stock table with specs (e.g., Socket type, VRAM).

3. Build a PC:

   Click "PC Builder" on the sidebar.

   Add Parts: Use the dropdown menu at the top to select a component (e.g., "Intel Core i9"). Click the "+ Add" button.

   Review: The component will appear in your "Current Build Configuration" list with its technical specs visible.

   Validate: Click the red "VALIDATE COMPATIBILITY" button.

     Success: A popup confirms all parts work together.

     Failure: A popup lists specific errors (e.g., "Socket Mismatch").

Option B: Using the Command Line (CLI)
1. Launch the App: Run python main.py in your terminal.

2. Main Menu Navigation:

    Enter 1 to Add Component: Follow the prompts to type in Name, Price, and Specs.

    Enter 2 to List Inventory: Displays a formatted ASCII table of all parts.

    Enter 3 to Create New Build (The Builder Mode).

3. Inside the Builder Mode:

    Select 1 to Add from Inventory: Choose parts by their ID number.

    Select 3 to View Current Build: See your "Shopping Cart" invoice.

    Select 4 to Validate Build: Runs the logic check and prints warnings to the screen.

Option C: Running Automated Tests
To demonstrate the validation logic programmatically (simulating incompatibilities like "Socket Mismatch" or "Power Overload") without manual input:
````bash
python test_scenarios.py
````
## OOP Principles Implemented
1. Abstraction: The HardwareComponent Abstract Base Class (ABC) defines the contract for all parts but cannot be instantiated itself.

2. Inheritance: Specific parts (CPU, GPU, Motherboard) inherit shared attributes (Price, Manufacturer) from the base class while extending it with unique fields (Sockets, VRam).

3. Polymorphism: The interface (both GUI and CLI) treats different objects uniformly when listing them, but the objects behave differently (e.g., displaying "Cores" for CPUs vs "VRAM" for GPUs) via method overriding.

4. Encapsulation: Data serialization logic (to_dict) is hidden inside the classes. The main application interacts with objects, not raw data.

5. Composition: The PCBuild class does not inherit from components; it contains them. This dynamic aggregation allows a build to consist of any combination of parts.


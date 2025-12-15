import sys
from src.models import CPU, GPU, Motherboard, RAM, PSU, Storage
from src.storage import InventoryManager
from src.build import PCBuild
from prettytable import PrettyTable
def print_menu():
    print("\n--- PC Builder CLI ---")
    print("1. Add Component to Inventory")
    print("2. List Inventory")
    print("3. Create New Build")
    print("4. Exit")

def get_input(prompt, type_=str):
    while True:
        try:
            value = input(prompt)
            if type_ == int:
                return int(value)
            elif type_ == float:
                return float(value)
            return value
        except ValueError:
            print(f"Invalid input. Please enter a valid {type_.__name__}.")

def add_component_menu(manager):
    print("\nSelect Component Type:")
    print("1. CPU")
    print("2. GPU")
    print("3. Motherboard")
    print("4. RAM")
    print("5. PSU")
    print("6. Storage")
    
    choice = get_input("Enter choice: ", int)
    
    name = get_input("Name: ")
    manufacturer = get_input("Manufacturer: ")
    price = get_input("Price: ", float)
    
    if choice == 1:
        cores = get_input("Cores: ", int)
        clock_speed = get_input("Clock Speed (GHz): ", float)
        socket = get_input("Socket: ")
        component = CPU(name, manufacturer, price, cores, clock_speed, socket)
    elif choice == 2:
        vram = get_input("VRAM (GB): ", int)
        core_clock = get_input("Core Clock (MHz): ", float)
        component = GPU(name, manufacturer, price, vram, core_clock)
    elif choice == 3:
        socket = get_input("Socket: ")
        form_factor = get_input("Form Factor: ")
        ram_slots = get_input("RAM Slots: ", int)
        memory_type = get_input("Memory Type (e.g. DDR4, DDR5): ")
        component = Motherboard(name, manufacturer, price, socket, form_factor, ram_slots, memory_type)
    elif choice == 4:
        size = get_input("Size (GB): ", int)
        speed = get_input("Speed (MHz): ", int)
        type_ = get_input("Type (e.g., DDR4): ")
        component = RAM(name, manufacturer, price, size, speed, type_)
    elif choice == 5:
        wattage = get_input("Wattage: ", int)
        rating = get_input("Rating (e.g., 80+ Gold): ")
        component = PSU(name, manufacturer, price, wattage, rating)
    elif choice == 6:
        capacity = get_input("Capacity (GB): ", int)
        type_ = get_input("Type (e.g., SSD, HDD): ")
        component = Storage(name, manufacturer, price, capacity, type_)
    else:
        print("Invalid choice.")
        return

    manager.add_item(component)
    print("Component added successfully!")

def list_inventory_menu(manager):
    items = manager.list_items()
    if not items:
        print("Inventory is empty.")
    # Create the table with professional headers
    table = PrettyTable()
    table.field_names = ["ID", "Category", "Manufacturer", "Name", "Price ($)", "Power (W)", "Key Specs"]
    
    # Align columns for better readability (Left align text, Right align numbers)
    table.align["Name"] = "l"
    table.align["Key Specs"] = "l"
    table.align["Price ($)"] = "r"

    for i, item in enumerate(items, 1):
        # Dynamic "Specs" formatting based on component type
        specs = ""
        if item.category == "CPU":
            specs = f"{item.cores} Cores, {item.clock_speed}GHz, {item.socket}"
        elif item.category == "GPU":
            specs = f"{item.vram}GB VRAM, {item.core_clock}MHz"
        elif item.category == "Motherboard":
            specs = f"{item.socket}, {item.form_factor}, {item.memory_type}"
        elif item.category == "RAM":
            specs = f"{item.size}GB {item.type}-{item.speed}"
        elif item.category == "PSU":
            specs = f"{item.wattage}W {item.rating}"
        elif item.category == "Storage":
            specs = f"{item.capacity}GB {item.type}"

        # Add the row
        table.add_row([
            i, 
            item.category, 
            item.manufacturer, 
            item.name, 
            f"{item.price:.2f}", 
            item.power_draw, 
            specs
        ])

    print(table)

def create_build_menu(manager):
    build = PCBuild()
    while True:
        print("\n--- Build Menu ---")
        print("1. Add Component from Inventory")
        print("2. Remove Component from Build")
        print("3. View Current Build")
        print("4. Validate Build")
        print("5. Finish Build (Back to Main Menu)")
        
        choice = get_input("Enter choice: ", int)
        
        if choice == 1:
            list_inventory_menu(manager)
            items = manager.list_items()
            if items:
                idx = get_input("Enter item number to add (0 to cancel): ", int)
                if 0 < idx <= len(items):
                    build.add_component(items[idx-1])
                    print("Component added to build.")
                elif idx != 0:
                    print("Invalid item number.")
        elif choice == 2:
            if not build.components:
                print("Build is empty.")
                continue
            for i, c in enumerate(build.components, 1):
                print(f"{i}. {c.name}")
            idx = get_input("Enter item number to remove (0 to cancel): ", int)
            if 0 < idx <= len(build.components):
                removed = build.components.pop(idx-1)
                print(f"Removed {removed.name} from build.")
            elif idx != 0:
                print("Invalid item number.")
        elif choice == 3:
            if not build.components:
                print("\n[!] Your build is currently empty.")
            else:
                print("\n--- Current Build Configuration ---")
                # Initialize the table
                build_table = PrettyTable()
                build_table.field_names = ["Category", "Manufacturer", "Component Name", "Price ($)"]
                
                # Alignments for a cleaner look
                build_table.align = "l"  # Left align everything by default
                build_table.align["Price ($)"] = "r"  # Right align prices
                
                # Add rows
                for component in build.components:
                    build_table.add_row([
                        component.category,
                        component.manufacturer,
                        component.name,
                        f"{component.price:.2f}"
                    ])
                
                print(build_table)
                
                # Print the total cost prominently
                total = build.total_cost()
                print(f"TOTAL BUILD COST: ${total:,.2f}")
                
                # Add a quick power check summary here for convenience
                total_power = sum(c.power_draw for c in build.components)
                print(f"ESTIMATED POWER DRAW: {total_power}W")
        elif choice == 4:
            valid, messages = build.validate_build()
            for msg in messages:
                print(msg)
        elif choice == 5:
            break
        else:
            print("Invalid choice.")

def main():
    manager = InventoryManager()
    
    while True:
        print_menu()
        choice = get_input("Enter choice: ", int)
        
        if choice == 1:
            add_component_menu(manager)
        elif choice == 2:
            list_inventory_menu(manager)
        elif choice == 3:
            create_build_menu(manager)
        elif choice == 4:
            print("Exiting...")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()

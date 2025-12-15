import json
import os
from .models import HardwareComponent, CPU, GPU, Motherboard, RAM, PSU, Storage

class InventoryManager:
    def __init__(self, file_path="data/inventory.json"):
        self.file_path = file_path
        self.inventory = []
        self.load_inventory()

    def load_inventory(self):
        if not os.path.exists(self.file_path):
            return

        try:
            with open(self.file_path, 'r') as f:
                data = json.load(f)
                for item_data in data:
                    category = item_data.get("category")
                    if category == "CPU":
                        self.inventory.append(CPU.from_dict(item_data))
                    elif category == "GPU":
                        self.inventory.append(GPU.from_dict(item_data))
                    elif category == "Motherboard":
                        self.inventory.append(Motherboard.from_dict(item_data))
                    elif category == "RAM":
                        self.inventory.append(RAM.from_dict(item_data))
                    elif category == "PSU":
                        self.inventory.append(PSU.from_dict(item_data))
                    elif category == "Storage":
                        self.inventory.append(Storage.from_dict(item_data))
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading inventory: {e}")

    def save_inventory(self):
        data = [item.to_dict() for item in self.inventory]
        try:
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            with open(self.file_path, 'w') as f:
                json.dump(data, f, indent=4)
        except IOError as e:
            print(f"Error saving inventory: {e}")

    def add_item(self, item: HardwareComponent):
        self.inventory.append(item)
        self.save_inventory()

    def remove_item(self, item_name: str):
        self.inventory = [item for item in self.inventory if item.name != item_name]
        self.save_inventory()

    def list_items(self):
        return self.inventory

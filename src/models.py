from abc import ABC, abstractmethod

class HardwareComponent(ABC):
    def __init__(self, name: str, manufacturer: str, price: float, category: str, power_draw=0):
        self.name = name
        self.manufacturer = manufacturer
        self.price = price
        self.category = category
        self.power_draw = power_draw

    def to_dict(self):
        return {
            "name": self.name,
            "manufacturer": self.manufacturer,
            "price": self.price,
            "category": self.category,
            "power_draw": self.power_draw
        }

    @classmethod
    def from_dict(cls, data):
        raise NotImplementedError("Subclasses must implement from_dict")

    def __str__(self):
        return f"{self.category}: {self.manufacturer} {self.name} - ${self.price:.2f}"


class CPU(HardwareComponent):
    def __init__(self, name, manufacturer, price, cores, clock_speed, socket, power_draw=105):           
        super().__init__(name, manufacturer, price, "CPU", power_draw)
        self.cores = cores
        self.clock_speed = clock_speed
        self.socket = socket

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "cores": self.cores,
            "clock_speed": self.clock_speed,
            "socket": self.socket
        })
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            manufacturer=data["manufacturer"],
            price=data["price"],
            cores=data["cores"],
            clock_speed=data["clock_speed"],
            socket=data["socket"],
            power_draw=data.get("power_draw", 105) 
        )


class GPU(HardwareComponent):
    def __init__(self, name, manufacturer, price, vram, core_clock, power_draw=250):
        super().__init__(name, manufacturer, price, "GPU", power_draw)
        self.vram = vram
        self.core_clock = core_clock

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "vram": self.vram,
            "core_clock": self.core_clock
        })
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            manufacturer=data["manufacturer"],
            price=data["price"],
            vram=data["vram"],
            core_clock=data["core_clock"],
            power_draw=data.get("power_draw", 250)
        )


class Motherboard(HardwareComponent):
    # Fixed: memory_type is before power_draw, and power_draw has default
    def __init__(self, name, manufacturer, price, socket, form_factor, ram_slots, memory_type, power_draw=50):
        super().__init__(name, manufacturer, price, "Motherboard", power_draw)
        self.socket = socket
        self.form_factor = form_factor
        self.ram_slots = ram_slots
        self.memory_type = memory_type  

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "socket": self.socket,
            "form_factor": self.form_factor,
            "ram_slots": self.ram_slots,
            "memory_type": self.memory_type
        })
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            manufacturer=data["manufacturer"],
            price=data["price"],
            socket=data["socket"],
            form_factor=data["form_factor"],
            ram_slots=data["ram_slots"],
            memory_type=data.get("memory_type", "DDR4"), # Default to DDR4 if missing
            power_draw=data.get("power_draw", 50)
        )


class RAM(HardwareComponent):
    def __init__(self, name, manufacturer, price, size, speed, type_, power_draw=5):
        super().__init__(name, manufacturer, price, "RAM", power_draw)
        self.size = size
        self.speed = speed
        self.type = type_

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "size": self.size,
            "speed": self.speed,
            "type": self.type
        })
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            manufacturer=data["manufacturer"],
            price=data["price"],
            size=data["size"],
            speed=data["speed"],
            type_=data["type"],
            power_draw=data.get("power_draw", 5)
        )


class PSU(HardwareComponent):
    def __init__(self, name, manufacturer, price, wattage, rating):
        # PSU supplies power, so we treat draw as 0
        super().__init__(name, manufacturer, price, "PSU", power_draw=0)
        self.wattage = wattage
        self.rating = rating

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "wattage": self.wattage,
            "rating": self.rating
        })
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            manufacturer=data["manufacturer"],
            price=data["price"],
            wattage=data["wattage"],
            rating=data["rating"]
        )


class Storage(HardwareComponent):
    def __init__(self, name, manufacturer, price, capacity, type_, power_draw=10):
        super().__init__(name, manufacturer, price, "Storage", power_draw)
        self.capacity = capacity
        self.type = type_

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "capacity": self.capacity,
            "type": self.type
        })
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            manufacturer=data["manufacturer"],
            price=data["price"],
            capacity=data["capacity"],
            type_=data["type"],
            power_draw=data.get("power_draw", 10)
        )
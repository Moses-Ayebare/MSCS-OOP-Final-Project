from .models import HardwareComponent, CPU, Motherboard, RAM, PSU

class PCBuild:
    def __init__(self):
        self.components = []

    def add_component(self, component: HardwareComponent):
        self.components.append(component)

    def remove_component(self, component_name: str):
        self.components = [c for c in self.components if c.name != component_name]

    def validate_build(self):
        messages = []
        cpu = next((c for c in self.components if isinstance(c, CPU)), None)
        motherboard = next((c for c in self.components if isinstance(c, Motherboard)), None)
        ram_list = [c for c in self.components if isinstance(c, RAM)]
        psu = next((c for c in self.components if isinstance(c, PSU)), None)
        if cpu and motherboard:
            if cpu.socket != motherboard.socket:
                messages.append(f"Incompatible: CPU socket {cpu.socket} does not match Motherboard socket {motherboard.socket}")

        # 2. RAM Compatibility Check
        if motherboard and ram_list:
            for ram in ram_list:
                if ram.type != motherboard.memory_type:
                     messages.append(f"CRITICAL: RAM type {ram.type} is not supported by Motherboard ({motherboard.memory_type})")

        # 3. Power Consumption Check
        total_draw = sum(c.power_draw for c in self.components)
        if psu:
            if total_draw > psu.wattage:
                messages.append(f"WARNING: Total power draw ({total_draw}W) exceeds PSU wattage ({psu.wattage}W)")
            # Standard advice: PSU should be 20% overhead
            elif total_draw > (psu.wattage * 0.8):
                messages.append(f"NOTE: Power draw ({total_draw}W) is close to PSU limit ({psu.wattage}W). Recommendation: Upgrade PSU.")
        elif total_draw > 0:
            messages.append("WARNING: No PSU selected to power these components.")
        
        
        
        if not messages:
            return True, ["Build is valid!"]
        return False, messages

    def total_cost(self):
        return sum(c.price for c in self.components)

    def __str__(self):
        return "\n".join([str(c) for c in self.components])

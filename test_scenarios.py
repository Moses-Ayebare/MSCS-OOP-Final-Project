# test_scenarios.py
import sys
from src.models import CPU, Motherboard, GPU, RAM, PSU
from src.build import PCBuild

def run_scenarios():
    print("\n==========================================")
    print("   PC Builder: Intelligent Validation Test   ")
    print("==========================================\n")

    # ---------------------------------------------------------
    # SCENARIO A: The "Socket Clash" (Intel CPU + AMD Mobo)
    # ---------------------------------------------------------
    print("TEST A: Socket Compatibility Check...")
    build_a = PCBuild()
    # Attempting to put an Intel 13th Gen (LGA1700) into an AMD Ryzen 
    # CPU: name, manufacturer, price, cores, clock, socket, power_draw
    build_a.add_component(CPU("Intel i9-13900K", "Intel", 580, 24, 5.8, "LGA1700", power_draw=125))
    # Mobo: name, manufacturer, price, socket, form_factor, ram_slots, memory_type, power_draw
    build_a.add_component(Motherboard("MSI B550", "MSI", 159, "AM4", "ATX", 4, "DDR4", power_draw=50))
    
    valid, msgs = build_a.validate_build()
    if not valid:
        print("SUCCESS: Incompatibility detected.")
        for m in msgs: print(f"   -> {m}")
    else:
        print("FAIL: Logic error. Build should have failed.")
    print("-" * 40)

    # ---------------------------------------------------------
    # SCENARIO B: The "Power Overload" (RTX 4090 + Weak PSU)
    # ---------------------------------------------------------
    print("\nTEST B: PSU Wattage Check...")
    build_b = PCBuild()
    # High-end components drawing ~635W total
    build_b.add_component(CPU("Intel i9-13900K", "Intel", 580, 24, 5.8, "LGA1700", power_draw=125))
    build_b.add_component(Motherboard("ASUS Z790", "ASUS", 499, "LGA1700", "ATX", 4, "DDR5", power_draw=60))
    build_b.add_component(GPU("Nvidia RTX 4090", "Nvidia", 1599, 24, 2520, power_draw=450))
    # Weak 500W PSU
    build_b.add_component(PSU("EVGA 500 W1", "EVGA", 49, 500, "80+ White"))

    valid, msgs = build_b.validate_build()
    # We expect warnings about power, even if valid returns True/False depending on strictness
    found_warning = any("exceeds PSU wattage" in m for m in msgs)
    
    if found_warning:
        print("SUCCESS: Power overload detected.")
        for m in msgs: print(f"   -> {m}")
    else:
        print("FAIL: Logic error. Should have warned about power.")
    print("-" * 40)

    # ---------------------------------------------------------
    # SCENARIO C: The "Generation Gap" (DDR4 RAM + DDR5 Mobo)
    # ---------------------------------------------------------
    print("\nTEST C: RAM Type Compatibility...")
    build_c = PCBuild()
    # Motherboard requires DDR5, but we are adding DDR4 RAM
    build_c.add_component(Motherboard("ASUS Z790", "ASUS", 499, "LGA1700", "ATX", 4, "DDR5", power_draw=60))
    build_c.add_component(RAM("G.Skill Ripjaws", "G.Skill", 49, 16, 3200, "DDR4", power_draw=10))

    valid, msgs = build_c.validate_build()
    if not valid:
        print("SUCCESS: RAM mismatch detected.")
        for m in msgs: print(f"   -> {m}")
    else:
        print("FAIL: Logic error. Should have flagged DDR4/DDR5 mismatch.")
    print("==========================================\n")

if __name__ == "__main__":
    run_scenarios()
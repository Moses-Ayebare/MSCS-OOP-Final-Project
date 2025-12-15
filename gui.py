import customtkinter as ctk
from tkinter import messagebox
from src.models import CPU, GPU, Motherboard, RAM, PSU, Storage
from src.storage import InventoryManager
from src.build import PCBuild

# --- Configuration ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class PCBuilderGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title("PC Builder: Intelligent Builder")
        self.geometry("1100x700")

        # Backend Connection        
        self.manager = InventoryManager()
        self.current_build = PCBuild()

        # Layout: Grid (2 Columns: Sidebar + Main Area)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        #Sidebar
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo = ctk.CTkLabel(self.sidebar, text="PC Builder", font=ctk.CTkFont(size=24, weight="bold"))
        self.logo.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Navigation Buttons
        self.btn_inv = ctk.CTkButton(self.sidebar, text="Inventory View", command=self.show_inventory)
        self.btn_inv.grid(row=1, column=0, padx=20, pady=10)
        
        self.btn_build = ctk.CTkButton(self.sidebar, text="PC Builder", fg_color="green", command=self.show_builder)
        self.btn_build.grid(row=2, column=0, padx=20, pady=10)

        # Main Area (Tabview) 
        # We use a TabView but hide the tabs to control it via Sidebar buttons
        self.tab_view = ctk.CTkTabview(self, width=850)
        self.tab_view.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        self.tab_inv = self.tab_view.add("Inventory")
        self.tab_build = self.tab_view.add("Builder")

        # Initialize Views
        self.setup_inventory_tab()
        self.setup_builder_tab()

        # Select first tab
        self.tab_view.set("Inventory")

    #  TAB 1: INVENTORY VIEWER
    def setup_inventory_tab(self):
        # Refresh Button
        self.btn_refresh = ctk.CTkButton(self.tab_inv, text="Refresh Data", command=self.refresh_inventory_list)
        self.btn_refresh.pack(pady=10)

        # Scrollable List
        self.inv_frame = ctk.CTkScrollableFrame(self.tab_inv, label_text="Current Stock")
        self.inv_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.refresh_inventory_list()

    def refresh_inventory_list(self):
        # Clear old widgets
        for widget in self.inv_frame.winfo_children():
            widget.destroy()
            
        items = self.manager.list_items()
        
        # Headers
        header_text = f"{'TYPE':<12} | {'NAME':<30} | {'PRICE':<10} | {'SPECS'}"
        ctk.CTkLabel(self.inv_frame, text=header_text, font=("Consolas", 14, "bold")).pack(anchor="w", padx=5)

        # Rows
        for item in items:
            # Polymorphic spec string
            specs = self.get_specs_string(item)
            row_text = f"{item.category:<12} | {item.name:<30} | ${item.price:<9.2f} | {specs}"
            
            btn = ctk.CTkButton(self.inv_frame, text=row_text, 
                                font=("Consolas", 12), fg_color="transparent", 
                                border_width=1, anchor="w", text_color="#ddd")
            btn.pack(fill="x", pady=2)

    def get_specs_string(self, item):
        # Helper to format specs for GUI
        if isinstance(item, CPU): return f"{item.socket}, {item.cores} Cores"
        if isinstance(item, GPU): return f"{item.vram}GB VRAM"
        if isinstance(item, Motherboard): return f"{item.socket}, {item.memory_type}"
        if isinstance(item, RAM): return f"{item.type} {item.speed}MHz"
        if isinstance(item, PSU): return f"{item.wattage}W"
        return ""

    # TAB 2: PC BUILDER & VALIDATOR
    def setup_builder_tab(self):
        # 1. Selection Area (Top)
        select_frame = ctk.CTkFrame(self.tab_build)
        select_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(select_frame, text="Add Component to Build:").pack(side="left", padx=10)
        
        # Dropdown to pick items
        self.component_var = ctk.StringVar(value="Select a component...")
        self.component_dropdown = ctk.CTkOptionMenu(select_frame, variable=self.component_var, width=400)
        self.component_dropdown.pack(side="left", padx=10)
        
        btn_add = ctk.CTkButton(select_frame, text="+ Add", width=80, command=self.add_to_build)
        btn_add.pack(side="left", padx=10)

        # Populate Dropdown
        self.update_dropdown()

        # 2. Build List (Middle)
        self.build_list_frame = ctk.CTkScrollableFrame(self.tab_build, label_text="Current Build Configuration")
        self.build_list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # 3. Action Area (Bottom)
        action_frame = ctk.CTkFrame(self.tab_build, height=100)
        action_frame.pack(fill="x", padx=10, pady=10)

        self.lbl_total = ctk.CTkLabel(action_frame, text="Total: $0.00", font=("Arial", 18, "bold"))
        self.lbl_total.pack(side="left", padx=20)
        
        self.lbl_power = ctk.CTkLabel(action_frame, text="Power: 0W", font=("Arial", 14), text_color="yellow")
        self.lbl_power.pack(side="left", padx=20)

        # THE BIG VALIDATE BUTTON
        btn_validate = ctk.CTkButton(action_frame, text="VALIDATE COMPATIBILITY", 
                                     fg_color="#D32F2F", hover_color="#B71C1C", 
                                     font=("Arial", 14, "bold"),
                                     command=self.run_validation)
        btn_validate.pack(side="right", padx=20, pady=10)

        # Clear Button
        ctk.CTkButton(action_frame, text="Clear Build", fg_color="#555", command=self.clear_build).pack(side="right", padx=10)

    def update_dropdown(self):
        # Load items from manager into the dropdown
        items = self.manager.list_items()
        if not items:
            self.component_dropdown.configure(values=["Inventory Empty"])
            return
            
        # NEW FORMAT: "ID: [Category] Name ($Price) - {SPECS}"
        values = []
        for i, item in enumerate(items):
            specs = self.get_specs_string(item)
            # Truncate name if it's too long to keep the dropdown clean
            name_short = (item.name[:25] + '..') if len(item.name) > 25 else item.name
            
            label = f"{i}: [{item.category}] {name_short} (${item.price}) - {specs}"
            values.append(label)

        self.component_dropdown.configure(values=values)

    def add_to_build(self):
        selection = self.component_var.get()
        if "Select" in selection or "Empty" in selection:
            return

        # Extract Index from string "0: CPU..."
        idx = int(selection.split(":")[0])
        item = self.manager.list_items()[idx]
        
        # Add to PCBuild Object
        self.current_build.add_component(item)
        self.refresh_build_view()

    def clear_build(self):
        self.current_build = PCBuild()
        self.refresh_build_view()

    def refresh_build_view(self):
        # Clear UI list
        for widget in self.build_list_frame.winfo_children():
            widget.destroy()

        if not self.current_build.components:
             ctk.CTkLabel(self.build_list_frame, text="Build is empty. Add parts above!", 
                          text_color="gray").pack(pady=20)
             return

        # Re-draw list with SPECS
        for item in self.current_build.components:
            f = ctk.CTkFrame(self.build_list_frame)
            f.pack(fill="x", pady=2)
            
            # 1. Category & Name
            ctk.CTkLabel(f, text=f"[{item.category}] {item.name}", 
                         width=250, anchor="w", font=("Arial", 12, "bold")).pack(side="left", padx=5)
            
            # 2. THE NEW SPECS COLUMN (Gray color to distinguish context)
            specs = self.get_specs_string(item)
            ctk.CTkLabel(f, text=specs, width=200, anchor="w", 
                         text_color="#AAAAAA", font=("Consolas", 11)).pack(side="left", padx=5)

            # 3. Price
            ctk.CTkLabel(f, text=f"${item.price}", width=80, anchor="e").pack(side="left", padx=10)
            
            # 4. Remove Button
            btn_del = ctk.CTkButton(f, text="X", width=30, fg_color="#C62828", hover_color="#B71C1C",
                                    command=lambda x=item.name: self.remove_from_build(x))
            btn_del.pack(side="right", padx=5)

        # Update Totals (Bottom Bar)
        self.lbl_total.configure(text=f"Total: ${self.current_build.total_cost():,.2f}")
        
        total_power = sum(c.power_draw for c in self.current_build.components)
        self.lbl_power.configure(text=f"Est. Power: {total_power}W")
    def remove_from_build(self, name):
        self.current_build.remove_component(name)
        self.refresh_build_view()

    def run_validation(self):
        if not self.current_build.components:
            messagebox.showwarning("Empty", "Add components before validating.")
            return

        # CALL THE BACKEND LOGIC (The same one used in CLI!)
        is_valid, messages = self.current_build.validate_build()
        
        # Format the report
        report = "\n".join(messages)
        
        if is_valid:
            messagebox.showinfo("Validation Success", f"Build is Compatible!\n\n{report}")
        else:
            messagebox.showerror("Incompatible Build", f"Issues Found:\n\n{report}")

    # NAVIGATION
    def show_inventory(self):
        self.tab_view.set("Inventory")

    def show_builder(self):
        self.tab_view.set("Builder")

if __name__ == "__main__":
    app = PCBuilderGUI()
    app.mainloop()
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from datetime import datetime

JSON_FOLDER = "json"

class MacroTrackerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Macro Tracker")
        self.geometry("1000x700")
        self.configure(bg="#2e2e2e")

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background="#2e2e2e")
        style.configure("TLabel", background="#2e2e2e", foreground="white")
        style.configure("TButton", background="#3e3e3e", foreground="white")
        style.map("TButton", background=[("active", "#555555")])
        style.configure("Treeview", background="#2e2e2e", fieldbackground="#2e2e2e", foreground="white")

        # Load persistent data from JSON files
        self.foods = self.load_data(os.path.join(JSON_FOLDER, "foods.json"))
        self.drinks = self.load_data(os.path.join(JSON_FOLDER, "drinks.json"))
        self.history = self.load_history(os.path.join(JSON_FOLDER, "history.json"))
        self.profile_history = self.load_profile_history(os.path.join(JSON_FOLDER, "profile_history.json"))
        self.profile_settings = self.load_profile_settings(os.path.join(JSON_FOLDER, "profile_settings.json"))
        self.goals = self.load_goals(os.path.join(JSON_FOLDER, "goals.json"))
        self.saved_meals = self.load_meals(os.path.join(JSON_FOLDER, "meals.json"))
        self.measurements = self.load_measurements(os.path.join(JSON_FOLDER, "measurements.json"))

        # Load or initialize daily data (including events)
        self.daily_data = self.load_daily_data(os.path.join(JSON_FOLDER, "daily.json"))
        today = datetime.now().strftime("%m/%d/%Y")
        if self.daily_data["date"] != today:
            if any(self.daily_data["totals"].values()):
                record = {
                    "date": self.daily_data["date"],
                    "calories": round(self.daily_data["totals"]["calories"], 1),
                    "protein": round(self.daily_data["totals"]["protein"], 1),
                    "carbs": round(self.daily_data["totals"]["carbs"], 1),
                    "fats": round(self.daily_data["totals"]["fats"], 1),
                    "calories_goal": self.goals["calories"],
                    "protein_goal": self.goals["protein"],
                    "carbs_goal": self.goals["carbs"],
                    "fats_goal": self.goals["fats"]
                }
                self.history.append(record)
                self.save_history(os.path.join(JSON_FOLDER, "history.json"))
            self.daily_data["date"] = today
            self.daily_data["totals"] = {"calories": 0, "protein": 0, "carbs": 0, "fats": 0}
            self.daily_data["events"] = []
            self.save_daily_data(os.path.join(JSON_FOLDER, "daily.json"))
        self.daily_totals = self.daily_data["totals"]

        notebook = ttk.Notebook(self)
        notebook.pack(expand=True, fill="both")

        # Tab Creation
        self.home_tab = ttk.Frame(notebook)
        self.today_tab = ttk.Frame(notebook)
        self.foods_tab = ttk.Frame(notebook)
        self.meals_tab = ttk.Frame(notebook)
        self.drinks_tab = ttk.Frame(notebook)
        self.history_tab = ttk.Frame(notebook)
        self.measurements_tab = ttk.Frame(notebook)
        self.profile_tab = ttk.Frame(notebook)

        notebook.add(self.home_tab, text="Home")
        notebook.add(self.today_tab, text="Today")
        notebook.add(self.foods_tab, text="Foods")
        notebook.add(self.meals_tab, text="Meals")
        notebook.add(self.drinks_tab, text="Drinks")
        notebook.add(self.history_tab, text="History")
        notebook.add(self.measurements_tab, text="Measurements")
        notebook.add(self.profile_tab, text="Profile")

        self.create_home_tab()
        self.create_today_tab()
        self.create_foods_tab()
        self.create_meals_tab()
        self.create_drinks_tab()
        self.create_history_tab()
        self.create_measurements_tab()
        self.create_profile_tab()

    # ----- Daily Data Persistence -----
    def load_daily_data(self, filename):
        if os.path.exists(filename):
            try:
                with open(filename, "r") as f:
                    data = json.load(f)
                if "events" not in data:
                    data["events"] = []
                return data
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load daily data: {e}")
                return {"date": datetime.now().strftime("%m/%d/%Y"),
                        "totals": {"calories": 0, "protein": 0, "carbs": 0, "fats": 0},
                        "events": []}
        else:
            return {"date": datetime.now().strftime("%m/%d/%Y"),
                    "totals": {"calories": 0, "protein": 0, "carbs": 0, "fats": 0},
                    "events": []}

    def save_daily_data(self, filename):
        try:
            with open(filename, "w") as f:
                json.dump(self.daily_data, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save daily data: {e}")

    # ----- Other Data Persistence Methods -----
    def load_data(self, filename):
        if os.path.exists(filename):
            try:
                with open(filename, "r") as f:
                    return json.load(f)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load {filename}: {e}")
                return []
        else:
            return []

    def load_history(self, filename):
        return self.load_data(filename)

    def save_history(self, filename):
        try:
            with open(filename, "w") as f:
                json.dump(self.history, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save history: {e}")

    def load_profile_history(self, filename):
        return self.load_data(filename)

    def save_profile_history(self, filename):
        try:
            with open(filename, "w") as f:
                json.dump(self.profile_history, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save profile history: {e}")

    def load_profile_settings(self, filename):
        if os.path.exists(filename):
            try:
                with open(filename, "r") as f:
                    return json.load(f)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load profile settings: {e}")
                return {}
        else:
            return {}

    def save_profile_settings(self, filename):
        try:
            with open(filename, "w") as f:
                json.dump(self.profile_settings, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save profile settings: {e}")

    def load_goals(self, filename):
        if os.path.exists(filename):
            try:
                with open(filename, "r") as f:
                    return json.load(f)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load goals from {filename}: {e}")
                return {"calories": 2000, "protein": 150, "carbs": 250, "fats": 70}
        else:
            return {"calories": 2000, "protein": 150, "carbs": 250, "fats": 70}

    def save_goals_to_file(self, filename):
        try:
            with open(filename, "w") as f:
                json.dump(self.goals, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save goals to {filename}: {e}")

    def load_meals(self, filename):
        if os.path.exists(filename):
            try:
                with open(filename, "r") as f:
                    return json.load(f)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load meals from {filename}: {e}")
                return []
        else:
            return []

    def save_meals_to_file(self, filename):
        try:
            with open(filename, "w") as f:
                json.dump(self.saved_meals, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save meals to {filename}: {e}")

    def load_measurements(self, filename):
        if os.path.exists(filename):
            try:
                with open(filename, "r") as f:
                    return json.load(f)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load measurements from {filename}: {e}")
                return []
        else:
            return []

    def save_measurements(self, filename):
        try:
            with open(filename, "w") as f:
                json.dump(self.measurements, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save measurements to {filename}: {e}")

    # ----- Today Tab -----
    def create_today_tab(self):
        frame = self.today_tab
        label = ttk.Label(frame, text="Today's Consumption History", font=("TkDefaultFont", 12, "bold"))
        label.pack(padx=5, pady=5)
        self.today_listbox = tk.Listbox(frame)
        self.today_listbox.pack(fill="both", expand=True, padx=10, pady=10)
        self.update_today_history_display()

    def log_event(self, event_str):
        self.daily_data["events"].append(event_str)
        self.save_daily_data(os.path.join(JSON_FOLDER, "daily.json"))
        self.update_today_history_display()

    def update_today_history_display(self):
        self.today_listbox.delete(0, tk.END)
        for event in self.daily_data["events"]:
            self.today_listbox.insert(tk.END, event)

    # ----- Home Tab -----
    def create_home_tab(self):
        frame = self.home_tab
        goals_frame = ttk.LabelFrame(frame, text="Daily Macro Goals", padding=10)
        goals_frame.pack(padx=10, pady=10, fill="x")
        self.goal_vars = {}
        row = 0
        for macro in ["calories", "protein", "carbs", "fats"]:
            ttk.Label(goals_frame, text=f"{macro.capitalize()}:").grid(row=row, column=0, sticky="w", padx=5, pady=5)
            var = tk.StringVar(value=str(self.goals[macro]))
            entry = ttk.Entry(goals_frame, textvariable=var, width=10)
            entry.grid(row=row, column=1, padx=5, pady=5)
            self.goal_vars[macro] = var
            row += 1
        save_button = ttk.Button(goals_frame, text="Save Goals", 
                                 command=lambda: self.save_goals_to_file(os.path.join(JSON_FOLDER, "goals.json")) or self.save_goals())
        save_button.grid(row=row, column=0, columnspan=2, pady=10)
        totals_frame = ttk.LabelFrame(frame, text="Today's Intake", padding=10)
        totals_frame.pack(padx=10, pady=10, fill="x")
        self.totals_labels = {}
        row = 0
        for macro in ["calories", "protein", "carbs", "fats"]:
            ttk.Label(totals_frame, text=f"{macro.capitalize()}:").grid(row=row, column=0, sticky="w", padx=5, pady=5)
            label = ttk.Label(totals_frame, text=f"{self.daily_totals[macro]:.1f}")
            label.grid(row=row, column=1, padx=5, pady=5)
            self.totals_labels[macro] = label
            row += 1

    def save_goals(self):
        for macro, var in self.goal_vars.items():
            try:
                self.goals[macro] = float(var.get())
            except ValueError:
                messagebox.showerror("Invalid Input", f"Please enter a valid number for {macro}.")
                return
        self.save_goals_to_file(os.path.join(JSON_FOLDER, "goals.json"))
        messagebox.showinfo("Goals Saved", "Daily goals updated and saved successfully.")

    def update_totals_display(self):
        for macro, label in self.totals_labels.items():
            label.config(text=f"{self.daily_totals[macro]:.1f}")

    def add_consumption(self, consumption):
        for macro in self.daily_totals:
            self.daily_totals[macro] += consumption.get(macro, 0)
            self.daily_data["totals"][macro] = self.daily_totals[macro]
        self.update_totals_display()
        self.save_daily_data(os.path.join(JSON_FOLDER, "daily.json"))

    # ----- Foods Tab -----
    def create_foods_tab(self):
        frame = self.foods_tab
        search_frame = ttk.Frame(frame)
        search_frame.pack(padx=10, pady=5, fill="x")
        ttk.Label(search_frame, text="Search Foods:").pack(side="left", padx=5)
        self.foods_search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.foods_search_var)
        search_entry.pack(side="left", padx=5, fill="x", expand=True)
        search_entry.bind("<KeyRelease>", lambda event: self.update_foods_list())
        self.foods_canvas = tk.Canvas(frame, bg="#2e2e2e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.foods_canvas.yview)
        self.foods_canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.foods_canvas.pack(side="left", fill="both", expand=True)
        self.foods_scrollable_frame = ttk.Frame(self.foods_canvas)
        self.foods_canvas.create_window((0, 0), window=self.foods_scrollable_frame, anchor="nw")
        self.foods_scrollable_frame.bind("<Configure>",
            lambda e: self.foods_canvas.configure(scrollregion=self.foods_canvas.bbox("all")))
        self.update_foods_list()

    def update_foods_list(self):
        for widget in self.foods_scrollable_frame.winfo_children():
            widget.destroy()
        query = self.foods_search_var.get().lower()
        for food in self.foods:
            if query and query not in food.get("name", "").lower():
                continue
            food_frame = ttk.Frame(self.foods_scrollable_frame, padding=10)
            food_frame.pack(fill="x", padx=5, pady=5)
            name = food.get("name", "Unknown")
            calories = food.get("calories", 0)
            protein = food.get("protein", 0)
            carbs = food.get("carbs", 0)
            fats = food.get("fats", 0)
            if food.get("per_unit", False):
                info = f"{name} - per unit: {calories} kcal, {protein}g protein, {carbs}g carbs, {fats}g fats"
            else:
                info = f"{name} - per 100g: {calories} kcal, {protein}g protein, {carbs}g carbs, {fats}g fats"
            ttk.Label(food_frame, text=info).pack(side="left", padx=5)
            action_button = ttk.Button(food_frame, text="I ate this",
                                       command=lambda f=food: self.record_food(f))
            action_button.pack(side="right", padx=5)

    def record_food(self, food):
        if food.get("per_unit", False):
            amount = simpledialog.askfloat("Food Quantity",
                                           f"Enter quantity (units) for {food.get('name', 'food')}:",
                                           minvalue=1, initialvalue=1)
            if amount is None:
                return
            consumption = {
                "calories": food.get("calories", 0) * amount,
                "protein": food.get("protein", 0) * amount,
                "carbs": food.get("carbs", 0) * amount,
                "fats": food.get("fats", 0) * amount,
            }
            event = f"Ate {amount:.1f} unit(s) of {food.get('name')}"
        else:
            amount = simpledialog.askfloat("Food Quantity",
                                           f"Enter amount (in grams) for {food.get('name', 'food')}:",
                                           minvalue=1, initialvalue=100)
            if amount is None:
                return
            factor = amount / 100.0
            consumption = {
                "calories": food.get("calories", 0) * factor,
                "protein": food.get("protein", 0) * factor,
                "carbs": food.get("carbs", 0) * factor,
                "fats": food.get("fats", 0) * factor,
            }
            event = f"Ate {amount:.1f}g of {food.get('name')}"
        self.add_consumption(consumption)
        self.log_event(event)
        messagebox.showinfo("Recorded", f"Recorded consumption for {food.get('name', 'food')}.")

    # ----- Meals Tab -----
    def create_meals_tab(self):
        frame = self.meals_tab
        new_meal_frame = ttk.LabelFrame(frame, text="Create New Meal", padding=10)
        new_meal_frame.pack(padx=10, pady=10, fill="x")
        ttk.Label(new_meal_frame, text="Meal Name:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.meal_name_var = tk.StringVar()
        meal_name_entry = ttk.Entry(new_meal_frame, textvariable=self.meal_name_var, width=30)
        meal_name_entry.grid(row=0, column=1, padx=5, pady=5)
        self.meal_builder_frame = ttk.Frame(new_meal_frame)
        self.meal_builder_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        self.meal_rows = []
        add_food_button = ttk.Button(new_meal_frame, text="Add Food", command=self.add_meal_row)
        add_food_button.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        save_meal_button = ttk.Button(new_meal_frame, text="Save Meal", command=self.save_current_meal)
        save_meal_button.grid(row=2, column=1, padx=5, pady=5, sticky="e")
        clear_meal_button = ttk.Button(new_meal_frame, text="Clear Meal", command=self.clear_meal_builder)
        clear_meal_button.grid(row=2, column=2, padx=5, pady=5, sticky="e")
        saved_meals_frame = ttk.LabelFrame(frame, text="Saved Meals", padding=10)
        saved_meals_frame.pack(padx=10, pady=10, fill="both", expand=True)
        self.meals_list_frame = ttk.Frame(saved_meals_frame)
        self.meals_list_frame.pack(fill="both", expand=True)
        self.update_saved_meals_display()

    def add_meal_row(self):
        row_frame = ttk.Frame(self.meal_builder_frame)
        row_frame.pack(fill="x", pady=2)
        food_names = [food.get("name", "Unknown") for food in self.foods]
        food_cb = ttk.Combobox(row_frame, values=food_names, state="readonly", width=25)
        food_cb.grid(row=0, column=0, padx=5)
        food_cb.set(food_names[0] if food_names else "")
        qty_entry = ttk.Entry(row_frame, width=10)
        qty_entry.grid(row=0, column=1, padx=5)
        qty_entry.insert(0, "100")
        remove_button = ttk.Button(row_frame, text="Remove", command=lambda: self.remove_meal_row(row_frame))
        remove_button.grid(row=0, column=2, padx=5)
        self.meal_rows.append({"frame": row_frame, "food_cb": food_cb, "qty_entry": qty_entry})

    def remove_meal_row(self, row_frame):
        for row in self.meal_rows:
            if row["frame"] == row_frame:
                self.meal_rows.remove(row)
                break
        row_frame.destroy()

    def save_current_meal(self):
        meal_name = self.meal_name_var.get().strip()
        if not meal_name:
            messagebox.showerror("Error", "Please enter a meal name.")
            return
        if not self.meal_rows:
            messagebox.showerror("Error", "Please add at least one food to the meal.")
            return
        items = []
        for row in self.meal_rows:
            food_name = row["food_cb"].get()
            try:
                qty = float(row["qty_entry"].get())
            except ValueError:
                messagebox.showerror("Error", f"Invalid quantity for {food_name}.")
                return
            food = next((f for f in self.foods if f.get("name") == food_name), None)
            if not food:
                messagebox.showerror("Error", f"Food '{food_name}' not found.")
                return
            items.append({"food": food, "quantity": qty})
        meal = {"name": meal_name, "items": items}
        self.saved_meals.append(meal)
        self.save_meals_to_file(os.path.join(JSON_FOLDER, "meals.json"))
        messagebox.showinfo("Meal Saved", f"Meal '{meal_name}' saved successfully.")
        self.clear_meal_builder()
        self.update_saved_meals_display()

    def clear_meal_builder(self):
        self.meal_name_var.set("")
        for row in self.meal_rows:
            row["frame"].destroy()
        self.meal_rows = []

    def update_saved_meals_display(self):
        for widget in self.meals_list_frame.winfo_children():
            widget.destroy()
        if not self.saved_meals:
            ttk.Label(self.meals_list_frame, text="No saved meals.").pack(padx=5, pady=5)
            return
        for meal in self.saved_meals:
            meal_frame = ttk.Frame(self.meals_list_frame, padding=5)
            meal_frame.pack(fill="x", pady=2)
            meal_label = ttk.Label(meal_frame, text=meal["name"], font=("TkDefaultFont", 10, "bold"))
            meal_label.pack(side="left", padx=5)
            view_button = ttk.Button(meal_frame, text="View Details", command=lambda m=meal: self.show_meal_details(m))
            view_button.pack(side="left", padx=5)
            record_button = ttk.Button(meal_frame, text="I ate this", command=lambda m=meal: self.record_meal(m))
            record_button.pack(side="right", padx=5)

    def show_meal_details(self, meal):
        details = f"Meal: {meal['name']}\n"
        for item in meal["items"]:
            food = item["food"]
            qty = item["quantity"]
            unit = "unit" if food.get("per_unit", False) else "g"
            details += f"- {food.get('name')}: {qty} {unit}\n"
        messagebox.showinfo("Meal Details", details)

    def record_meal(self, meal):
        total = {"calories": 0, "protein": 0, "carbs": 0, "fats": 0}
        for item in meal["items"]:
            food = item["food"]
            qty = item["quantity"]
            factor = qty if food.get("per_unit", False) else qty / 100.0
            total["calories"] += food.get("calories", 0) * factor
            total["protein"]  += food.get("protein", 0) * factor
            total["carbs"]    += food.get("carbs", 0) * factor
            total["fats"]     += food.get("fats", 0) * factor
        self.add_consumption(total)
        event = (f"Ate meal '{meal['name']}' (Cal: {round(total['calories'],1)}, "
                 f"Prot: {round(total['protein'],1)}, Carbs: {round(total['carbs'],1)}, "
                 f"Fats: {round(total['fats'],1)})")
        self.log_event(event)
        messagebox.showinfo("Meal Recorded", f"Recorded meal '{meal['name']}' with totals:\n"
                                              f"Calories: {round(total['calories'],1)}\n"
                                              f"Protein: {round(total['protein'],1)}\n"
                                              f"Carbs: {round(total['carbs'],1)}\n"
                                              f"Fats: {round(total['fats'],1)}")

    # ----- Drinks Tab -----
    def create_drinks_tab(self):
        frame = self.drinks_tab
        search_frame = ttk.Frame(frame)
        search_frame.pack(padx=10, pady=5, fill="x")
        ttk.Label(search_frame, text="Search Drinks:").pack(side="left", padx=5)
        self.drinks_search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.drinks_search_var)
        search_entry.pack(side="left", padx=5, fill="x", expand=True)
        search_entry.bind("<KeyRelease>", lambda event: self.update_drinks_list())
        self.drinks_canvas = tk.Canvas(frame, bg="#2e2e2e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.drinks_canvas.yview)
        self.drinks_canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.drinks_canvas.pack(side="left", fill="both", expand=True)
        self.drinks_scrollable_frame = ttk.Frame(self.drinks_canvas)
        self.drinks_canvas.create_window((0, 0), window=self.drinks_scrollable_frame, anchor="nw")
        self.drinks_scrollable_frame.bind("<Configure>",
            lambda e: self.drinks_canvas.configure(scrollregion=self.drinks_canvas.bbox("all")))
        self.update_drinks_list()

    def update_drinks_list(self):
        for widget in self.drinks_scrollable_frame.winfo_children():
            widget.destroy()
        query = self.drinks_search_var.get().lower()
        for drink in self.drinks:
            if query and query not in drink.get("name", "").lower():
                continue
            drink_frame = ttk.Frame(self.drinks_scrollable_frame, padding=10)
            drink_frame.pack(fill="x", padx=5, pady=5)
            name = drink.get("name", "Unknown")
            calories = drink.get("calories", 0)
            protein = drink.get("protein", 0)
            carbs = drink.get("carbs", 0)
            fats = drink.get("fats", 0)
            info = f"{name} - per serving: {calories} kcal, {protein}g protein, {carbs}g carbs, {fats}g fats"
            ttk.Label(drink_frame, text=info).pack(side="left", padx=5)
            action_button = ttk.Button(drink_frame, text="I drank this",
                                       command=lambda d=drink: self.record_drink(d))
            action_button.pack(side="right", padx=5)

    def record_drink(self, drink):
        consumption = {
            "calories": drink.get("calories", 0),
            "protein": drink.get("protein", 0),
            "carbs": drink.get("carbs", 0),
            "fats": drink.get("fats", 0),
        }
        self.add_consumption(consumption)
        event = f"Drank 1 serving of {drink.get('name')}"
        self.log_event(event)
        messagebox.showinfo("Recorded", f"Recorded 1 serving of {drink.get('name', 'drink')}.")

    # ----- History Tab -----
    def create_history_tab(self):
        frame = self.history_tab
        columns = ("date", "calories", "protein", "carbs", "fats")
        self.history_tree = ttk.Treeview(frame, columns=columns, show="headings")
        self.history_tree.heading("date", text="Date")
        self.history_tree.heading("calories", text="Calories")
        self.history_tree.heading("protein", text="Protein")
        self.history_tree.heading("carbs", text="Carbs")
        self.history_tree.heading("fats", text="Fats")
        self.history_tree.column("date", width=160)
        self.history_tree.column("calories", width=120)
        self.history_tree.column("protein", width=120)
        self.history_tree.column("carbs", width=120)
        self.history_tree.column("fats", width=120)
        self.history_tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.update_history_tab()

    def update_history_tab(self):
        for row in self.history_tree.get_children():
            self.history_tree.delete(row)
        for record in self.history:
            calories_str = f"{record.get('calories', 0):.1f} / {record.get('calories_goal', 0):.1f}"
            protein_str  = f"{record.get('protein', 0):.1f} / {record.get('protein_goal', 0):.1f}"
            carbs_str    = f"{record.get('carbs', 0):.1f} / {record.get('carbs_goal', 0):.1f}"
            fats_str     = f"{record.get('fats', 0):.1f} / {record.get('fats_goal', 0):.1f}"
            self.history_tree.insert("", "end", values=(
                record.get("date", ""),
                calories_str,
                protein_str,
                carbs_str,
                fats_str
            ))

    # ----- Measurements Tab -----
    def create_measurements_tab(self):
        frame = self.measurements_tab
        record_frame = ttk.LabelFrame(frame, text="Record New Measurements", padding=10)
        record_frame.pack(padx=10, pady=10, fill="x")
        self.measurements_vars = {}
        measurement_fields = [
            ("Left Bicep (cm)", "left_bicep"),
            ("Right Bicep (cm)", "right_bicep"),
            ("Shoulders (cm)", "shoulders"),
            ("Chest (cm)", "chest"),
            ("Waist (cm)", "waist"),
            ("Left Thigh (cm)", "left_thigh"),
            ("Right Thigh (cm)", "right_thigh"),
            ("Left Calf (cm)", "left_calf"),
            ("Right Calf (cm)", "right_calf")
        ]
        row = 0
        for label_text, key in measurement_fields:
            ttk.Label(record_frame, text=label_text + ":").grid(row=row, column=0, sticky="w", padx=5, pady=5)
            var = tk.StringVar()
            entry = ttk.Entry(record_frame, textvariable=var, width=10)
            entry.grid(row=row, column=1, padx=5, pady=5)
            self.measurements_vars[key] = var
            row += 1
        record_button = ttk.Button(record_frame, text="Record Measurements", command=self.record_measurements)
        record_button.grid(row=row, column=0, columnspan=2, pady=10)
        history_frame = ttk.LabelFrame(frame, text="Measurements History", padding=10)
        history_frame.pack(padx=10, pady=10, fill="both", expand=True)
        columns = ("date", "left_bicep", "right_bicep", "shoulders", "chest", "waist", "left_thigh", "right_thigh", "left_calf", "right_calf")
        self.measurements_tree = ttk.Treeview(history_frame, columns=columns, show="headings")
        for col in columns:
            self.measurements_tree.heading(col, text=col.replace("_", " ").capitalize())
            self.measurements_tree.column(col, width=100)
        self.measurements_tree.pack(fill="both", expand=True, padx=5, pady=5)
        self.update_measurements_tree()

    def record_measurements(self):
        date_str = datetime.now().strftime("%m/%d/%Y")
        try:
            left_bicep = float(self.measurements_vars["left_bicep"].get())
            right_bicep = float(self.measurements_vars["right_bicep"].get())
            shoulders = float(self.measurements_vars["shoulders"].get())
            chest = float(self.measurements_vars["chest"].get())
            waist = float(self.measurements_vars["waist"].get())
            left_thigh = float(self.measurements_vars["left_thigh"].get())
            right_thigh = float(self.measurements_vars["right_thigh"].get())
            left_calf = float(self.measurements_vars["left_calf"].get())
            right_calf = float(self.measurements_vars["right_calf"].get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for all measurements.")
            return
        record = {
            "date": date_str,
            "left_bicep": round(left_bicep, 1),
            "right_bicep": round(right_bicep, 1),
            "shoulders": round(shoulders, 1),
            "chest": round(chest, 1),
            "waist": round(waist, 1),
            "left_thigh": round(left_thigh, 1),
            "right_thigh": round(right_thigh, 1),
            "left_calf": round(left_calf, 1),
            "right_calf": round(right_calf, 1)
        }
        self.measurements.append(record)
        self.save_measurements(os.path.join(JSON_FOLDER, "measurements.json"))
        self.update_measurements_tree()
        messagebox.showinfo("Measurements Recorded", "Your measurements have been recorded.")

    def update_measurements_tree(self):
        for row in self.measurements_tree.get_children():
            self.measurements_tree.delete(row)
        for record in self.measurements:
            self.measurements_tree.insert("", "end", values=(
                record.get("date", ""),
                f"{record.get('left_bicep', 0):.1f}",
                f"{record.get('right_bicep', 0):.1f}",
                f"{record.get('shoulders', 0):.1f}",
                f"{record.get('chest', 0):.1f}",
                f"{record.get('waist', 0):.1f}",
                f"{record.get('left_thigh', 0):.1f}",
                f"{record.get('right_thigh', 0):.1f}",
                f"{record.get('left_calf', 0):.1f}",
                f"{record.get('right_calf', 0):.1f}"
            ))

    # ----- Profile Tab -----
    def create_profile_tab(self):
        frame = self.profile_tab
        settings_frame = ttk.LabelFrame(frame, text="Profile Settings (Static)", padding=10)
        settings_frame.pack(padx=10, pady=10, fill="x")
        self.settings_vars = {}
        row = 0
        for label_text, key in [("Age", "age"), ("Height (cm)", "height")]:
            ttk.Label(settings_frame, text=f"{label_text}:").grid(row=row, column=0, sticky="w", padx=5, pady=5)
            var = tk.StringVar(value=str(self.profile_settings.get(key, "")))
            entry = ttk.Entry(settings_frame, textvariable=var, width=10)
            entry.grid(row=row, column=1, padx=5, pady=5)
            self.settings_vars[key] = var
            row += 1
        save_settings_button = ttk.Button(settings_frame, text="Save Settings", 
                                          command=lambda: self.save_profile_settings(os.path.join(JSON_FOLDER, "profile_settings.json")) or self.save_profile_settings_ui())
        save_settings_button.grid(row=row, column=0, columnspan=2, pady=10)
        dynamic_frame = ttk.LabelFrame(frame, text="Daily Update", padding=10)
        dynamic_frame.pack(padx=10, pady=10, fill="x")
        self.dynamic_vars = {}
        row = 0
        for label_text, key in [("Weight (kg)", "weight"), ("Bodyfat (%)", "bodyfat")]:
            ttk.Label(dynamic_frame, text=f"{label_text}:").grid(row=row, column=0, sticky="w", padx=5, pady=5)
            var = tk.StringVar()
            entry = ttk.Entry(dynamic_frame, textvariable=var, width=10)
            entry.grid(row=row, column=1, padx=5, pady=5)
            self.dynamic_vars[key] = var
            row += 1
        record_update_button = ttk.Button(dynamic_frame, text="Record Update", command=self.record_profile_update)
        record_update_button.grid(row=row, column=0, columnspan=2, pady=10)
        history_frame = ttk.LabelFrame(frame, text="Profile History (Weight & Bodyfat)", padding=10)
        history_frame.pack(padx=10, pady=10, fill="both", expand=True)
        columns = ("date", "weight", "bodyfat")
        self.profile_tree = ttk.Treeview(history_frame, columns=columns, show="headings")
        self.profile_tree.heading("date", text="Date")
        self.profile_tree.heading("weight", text="Weight (kg)")
        self.profile_tree.heading("bodyfat", text="Bodyfat (%)")
        self.profile_tree.column("date", width=160)
        self.profile_tree.column("weight", width=100)
        self.profile_tree.column("bodyfat", width=100)
        self.profile_tree.pack(fill="both", expand=True, padx=5, pady=5)
        self.update_profile_tree()

    def save_profile_settings_ui(self):
        try:
            age = int(self.settings_vars["age"].get())
            height = float(self.settings_vars["height"].get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for age and height.")
            return
        self.profile_settings["age"] = age
        self.profile_settings["height"] = height
        self.save_profile_settings(os.path.join(JSON_FOLDER, "profile_settings.json"))
        messagebox.showinfo("Settings Saved", "Profile settings saved successfully.")

    def record_profile_update(self):
        try:
            weight = float(self.dynamic_vars["weight"].get())
            bodyfat_str = self.dynamic_vars["bodyfat"].get().strip()
            bodyfat = float(bodyfat_str) if bodyfat_str else None
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for weight and bodyfat.")
            return
        record = {
            "date": datetime.now().strftime("%m/%d/%Y"),
            "weight": weight,
            "bodyfat": bodyfat if bodyfat is not None else ""
        }
        self.profile_history.append(record)
        self.save_profile_history(os.path.join(JSON_FOLDER, "profile_history.json"))
        self.update_profile_tree()
        messagebox.showinfo("Update Recorded", "Profile update recorded successfully.")

    def update_profile_tree(self):
        for row in self.profile_tree.get_children():
            self.profile_tree.delete(row)
        for record in self.profile_history:
            self.profile_tree.insert("", "end", values=(
                record.get("date", ""),
                record.get("weight", ""),
                record.get("bodyfat", "")
            ))

if __name__ == "__main__":
    app = MacroTrackerApp()
    app.mainloop()

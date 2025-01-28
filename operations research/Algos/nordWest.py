import random
import tkinter as tk
from tkinter import ttk, messagebox

def generate_random_costs(rows, cols):
    return [[random.randint(1, 20) for _ in range(cols)] for _ in range(rows)]

def northwest_corner_method(supply, demand, costs):
    rows, cols = len(supply), len(demand)
    allocation = [[0] * cols for _ in range(rows)]

    i, j = 0, 0
    while i < rows and j < cols:
        allocation[i][j] = min(supply[i], demand[j])
        if supply[i] < demand[j]:
            demand[j] -= supply[i]
            supply[i] = 0
            i += 1
        else:
            supply[i] -= demand[j]
            demand[j] = 0
            j += 1

    total_cost = sum(allocation[i][j] * costs[i][j] for i in range(rows) for j in range(cols))
    return allocation, total_cost

def display_results():
    try:
        # Getting user input for supply and demand
        supply_input = supply_entry.get()
        demand_input = demand_entry.get()

        # Convert input to lists of integers
        supply = list(map(int, supply_input.split()))
        demand = list(map(int, demand_input.split()))

        if len(supply) == 0 or len(demand) == 0:
            raise ValueError("Supply and demand lists cannot be empty.")

        rows, cols = len(supply), len(demand)
        costs = generate_random_costs(rows, cols)

        # Clear previous results
        for widget in result_frame.winfo_children():
            widget.destroy()

        # Display the cost matrix
        cost_label = ttk.Label(result_frame, text="Cost Matrix:", font=("Arial", 12, "bold"))
        cost_label.pack(pady=10)
        cost_frame = ttk.Frame(result_frame)
        cost_frame.pack(pady=10)

        for i in range(rows):
            for j in range(cols):
                ttk.Label(cost_frame, text=f"{costs[i][j]:>3}", relief="solid", width=5).grid(row=i, column=j, padx=5, pady=5)

        # Calculate allocation using Northwest Corner Method
        allocation, total_cost = northwest_corner_method(supply[:], demand[:], costs)

        allocation_label = ttk.Label(result_frame, text="Allocation Matrix:", font=("Arial", 12, "bold"))
        allocation_label.pack(pady=10)
        allocation_frame = ttk.Frame(result_frame)
        allocation_frame.pack(pady=10)

        for i in range(rows):
            for j in range(cols):
                ttk.Label(allocation_frame, text=f"{allocation[i][j]:>3}", relief="solid", width=5).grid(row=i, column=j, padx=5, pady=5)

        cost_summary = ttk.Label(result_frame, text=f"Total Cost: {total_cost}", font=("Arial", 12, "bold"))
        cost_summary.pack(pady=10)

    except ValueError as e:
        messagebox.showerror("Input Error", f"Invalid input: {str(e)}")

# Create rounded button
def create_rounded_button(master, text, command):
    button_frame = tk.Frame(master, bg="#F0F0F0", bd=0)  # Remove outer border from the button
    canvas = tk.Canvas(button_frame, width=150, height=40, bg="#F0F0F0", highlightthickness=0)
    rect = create_rounded_rectangle(canvas, 5, 5, 145, 35, radius=20, outline="#008080", width=2, fill="#E0F7FA")
    label = canvas.create_text(75, 20, text=text, font=("Arial", 10), fill="#008080")

    def on_click(event):
        command()
        # canvas.itemconfig(rect, fill="#4CAF50")  # Green color for click

    def on_enter(event):
        canvas.itemconfig(rect, fill="#72BAA9")  # Coral color for hover

    def on_leave(event):
        canvas.itemconfig(rect, fill="#E0F7FA")  # Light blue color for default

    canvas.bind("<Button-1>", on_click)
    canvas.bind("<Enter>", on_enter)
    canvas.bind("<Leave>", on_leave)


    canvas.pack()
    button_frame.pack(pady=20)

# Create rounded rectangle
def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    points = [
        x1 + radius, y1,
        x1 + radius, y1,
        x2 - radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1 + radius,
        x1, y1,
    ]
    return canvas.create_polygon(points, **kwargs, smooth=True)

# Create the main window
def nordWest():
    global supply_entry, demand_entry, result_frame

    window = tk.Tk()
    window.title("Northwest Corner Method")

    # Outer border for the entire window
    outer_frame = tk.Frame(window, bg="#008080", bd=5)  # Outer border with desired color and width
    outer_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Create a canvas and a scrollbar inside the outer frame
    canvas = tk.Canvas(outer_frame)
    scrollbar = ttk.Scrollbar(outer_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Supply input
    supply_label = ttk.Label(scrollable_frame, text="Enter supply values (space separated):")
    supply_label.pack(pady=10)
    supply_entry = ttk.Entry(scrollable_frame, width=50)
    supply_entry.pack(pady=5)

    # Demand input
    demand_label = ttk.Label(scrollable_frame, text="Enter demand values (space separated):")
    demand_label.pack(pady=10)
    demand_entry = ttk.Entry(scrollable_frame, width=50)
    demand_entry.pack(pady=5)

    # Button to trigger result display
    create_rounded_button(scrollable_frame, "Calculate", display_results)

    # Frame to display results
    result_frame = ttk.Frame(scrollable_frame)
    result_frame.pack(pady=20)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    window.mainloop()

if __name__ == "__main__":
    nordWest()
import random
import tkinter as tk
from tkinter import ttk, messagebox

def generate_random_costs(rows, cols):
    return [[random.randint(1, 20) for _ in range(cols)] for _ in range(rows)]

def least_cost_method(supply, demand, costs):
    rows, cols = len(supply), len(demand)
    allocation = [[0] * cols for _ in range(rows)]

    while any(supply) and any(demand):
        # Find the minimum cost cell
        min_cost = float('inf')
        min_i, min_j = -1, -1
        for i in range(rows):
            for j in range(cols):
                if supply[i] > 0 and demand[j] > 0 and costs[i][j] < min_cost:
                    min_cost = costs[i][j]
                    min_i, min_j = i, j

        # Allocate as much as possible to the minimum cost cell
        allocation[min_i][min_j] = min(supply[min_i], demand[min_j])
        if supply[min_i] < demand[min_j]:
            demand[min_j] -= supply[min_i]
            supply[min_i] = 0
        else:
            supply[min_i] -= demand[min_j]
            demand[min_j] = 0

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

        # Display the cost matrix in a table format
        cost_label = ttk.Label(result_frame, text="Cost Matrix:", font=("Arial", 12, "bold"))
        cost_label.grid(row=0, column=0, columnspan=cols+1, pady=(0, 5))

        for i in range(rows):
            for j in range(cols):
                cost_value = costs[i][j]
                cell_label = ttk.Label(result_frame, text=cost_value, relief="solid", width=10, anchor="center")
                cell_label.grid(row=i+1, column=j, padx=5, pady=5)

        # Calculate the allocations using Least Cost Method
        least_allocation, least_total_cost = least_cost_method(supply[:], demand[:], costs)
        least_label = ttk.Label(result_frame, text="Result of Least Cost Method:", font=("Arial", 12, "bold"))
        least_label.grid(row=rows+1, column=0, columnspan=cols+1, pady=(10, 5))

        for i in range(rows):
            for j in range(cols):
                allocation_value = least_allocation[i][j]
                cell_label = ttk.Label(result_frame, text=allocation_value, relief="solid", width=10, anchor="center")
                cell_label.grid(row=rows+2+i, column=j, padx=5, pady=5)

        least_cost_label = ttk.Label(result_frame, text=f"Total Cost: {least_total_cost}", font=("Arial", 10))
        least_cost_label.grid(row=rows+2+rows, column=0, columnspan=cols+1, pady=(5, 10))

    except ValueError as e:
        messagebox.showerror("Error", f"Input error: {str(e)}")

def create_rounded_button(master, text, command):
    canvas = tk.Canvas(master, width=150, height=40, bg="#F0F0F0", highlightthickness=0)
    rect = create_rounded_rectangle(canvas, 5, 5, 145, 35, radius=20, outline="#008080", width=2, fill="#E0F7FA")
    label = canvas.create_text(75, 20, text=text, font=("Arial", 10), fill="#008080")

    def on_click(event):
        command()
        #canvas.itemconfig(rect, fill="#4CAF50")  # Green color for click

    def on_enter(event):
        canvas.itemconfig(rect, fill="#72BAA9")  # Coral color for hover

    def on_leave(event):
        canvas.itemconfig(rect, fill="#E0F7FA")  # Light blue color for default

    canvas.bind("<Button-1>", on_click)
    canvas.bind("<Enter>", on_enter)
    canvas.bind("<Leave>", on_leave)

    return canvas

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

def leastCostMethod():
    window = tk.Tk()
    window.title("Least Cost Method")

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

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Frame for input
    input_frame = ttk.Frame(scrollable_frame)
    input_frame.pack(pady=10)

    # Label for Supply input
    ttk.Label(input_frame, text="Enter supply values (space separated):").pack(pady=10)

    # Entry widget for Supply
    global supply_entry
    supply_entry = ttk.Entry(input_frame, width=30)
    supply_entry.pack(pady=5)

    # Label for Demand input
    ttk.Label(input_frame, text="Enter demand values (space separated):").pack(pady=10)

    # Entry widget for Demand
    global demand_entry
    demand_entry = ttk.Entry(input_frame, width=30)
    demand_entry.pack(pady=5)

    # Button to trigger result display
    create_rounded_button(scrollable_frame, "Generate Results", display_results).pack(pady=20)

    # Frame for results
    global result_frame
    result_frame = ttk.Frame(scrollable_frame, padding="10")
    result_frame.pack(fill="both", expand=True)

    window.mainloop()

if __name__ == "__main__":
    leastCostMethod()

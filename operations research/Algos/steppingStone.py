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

def stepping_stone_method(allocation, costs):
    rows, cols = len(allocation), len(allocation[0])
    def get_closed_path(allocation, start):
        visited = set()
        stack = [(start, [start])]
        while stack:
            (x, y), path = stack.pop()
            visited.add((x, y))
            if len(path) > 3 and path[0] == path[-1]:
                return path
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if (0 <= nx < rows and 0 <= ny < cols and (nx, ny) not in visited and allocation[nx][ny] != 0):
                    stack.append(((nx, ny), path + [(nx, ny)]))
        return []

    while True:
        u = [None] * rows
        v = [None] * cols
        u[0] = 0
        for _ in range(rows + cols):
            for i in range(rows):
                for j in range(cols):
                    if allocation[i][j] != 0:
                        if u[i] is not None and v[j] is None:
                            v[j] = costs[i][j] - u[i]
                        elif v[j] is not None and u[i] is None:
                            u[i] = costs[i][j] - v[j]

        opportunity_costs = [
            [costs[i][j] - (u[i] + v[j]) if u[i] is not None and v[j] is not None else None for j in range(cols)]
            for i in range(rows)
        ]
        min_cost = min((val for row in opportunity_costs for val in row if val is not None and val < 0), default=None)
        if min_cost is None:
            break
        min_cell = None
        for i in range(rows):
            for j in range(cols):
                if opportunity_costs[i][j] == min_cost:
                    min_cell = (i, j)
                    break
            if min_cell:
                break
        path = get_closed_path(allocation, min_cell)
        if not path:
            break
        min_alloc = min(allocation[x][y] for x, y in path[1::2])
        for i, (x, y) in enumerate(path):
            allocation[x][y] += min_alloc if i % 2 == 0 else -min_alloc
    total_cost = sum(allocation[i][j] * costs[i][j] for i in range(rows) for j in range(cols))
    return allocation, total_cost

def display_results(supply_entry, demand_entry):
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

        # Create the Tkinter window
        root = tk.Toplevel()
        root.title("Cost Allocation Methods Results")

        # Create a canvas and a scrollbar
        canvas = tk.Canvas(root)
        scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Create a frame within the canvas
        result_frame = ttk.Frame(canvas, padding="10")
        result_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Add the frame to the canvas
        canvas.create_window((0, 0), window=result_frame, anchor="nw")
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Display the cost matrix in a table format
        cost_label = ttk.Label(result_frame, text="Cost Matrix:", font=("Arial", 12, "bold"))
        cost_label.grid(row=0, column=0, columnspan=cols+1, pady=(0, 5))

        for i in range(rows):
            for j in range(cols):
                cost_value = costs[i][j]
                cell_label = ttk.Label(result_frame, text=cost_value, relief="solid", width=10, anchor="center")
                cell_label.grid(row=i+1, column=j, padx=5, pady=5)

        # Northwest Corner Method results
        nw_allocation, nw_total_cost = northwest_corner_method(supply[:], demand[:], costs)
        nw_label = ttk.Label(result_frame, text="Northwest Corner Method:", font=("Arial", 12, "bold"))
        nw_label.grid(row=rows+1, column=0, columnspan=cols+1, pady=(10, 5))

        for i in range(rows):
            for j in range(cols):
                allocation_value = nw_allocation[i][j]
                cell_label = ttk.Label(result_frame, text=allocation_value, relief="solid", width=10, anchor="center")
                cell_label.grid(row=rows+2+i, column=j, padx=5, pady=5)

        nw_cost_label = ttk.Label(result_frame, text=f"Total Cost: {nw_total_cost}", font=("Arial", 10))
        nw_cost_label.grid(row=rows+2+rows, column=0, columnspan=cols+1, pady=(5, 10))

        # Least Cost Method results
        least_allocation, least_total_cost = least_cost_method(supply[:], demand[:], costs)
        least_label = ttk.Label(result_frame, text="Least Cost Method:", font=("Arial", 12, "bold"))
        least_label.grid(row=rows+3+rows, column=0, columnspan=cols+1, pady=(10, 5))

        for i in range(rows):
            for j in range(cols):
                allocation_value = least_allocation[i][j]
                cell_label = ttk.Label(result_frame, text=allocation_value, relief="solid", width=10, anchor="center")
                cell_label.grid(row=rows+4+rows+i, column=j, padx=5, pady=5)

        least_cost_label = ttk.Label(result_frame, text=f"Total Cost: {least_total_cost}", font=("Arial", 10))
        least_cost_label.grid(row=rows+4+rows+rows, column=0, columnspan=cols+1, pady=(5, 10))

        # Optimal solution display
        if nw_total_cost < least_total_cost:
            optimal_allocation = nw_allocation
            optimal_cost = nw_total_cost
            optimal_label = ttk.Label(result_frame, text="Northwest Corner Method is optimal.", font=("Arial", 10, "italic"))
        else:
            optimal_allocation = least_allocation
            optimal_cost = least_total_cost
            optimal_label = ttk.Label(result_frame, text="Least Cost Method is optimal.", font=("Arial", 10, "italic"))

        optimal_label.grid(row=rows+5+rows*2, column=0, columnspan=cols+1, pady=(5, 10))

        # Stepping Stone Method results
        stepping_label = ttk.Label(result_frame, text="Applying Stepping Stone Method:", font=("Arial", 12, "bold"))
        stepping_label.grid(row=rows+6+rows*2, column=0, columnspan=cols+1, pady=(10, 5))

        final_allocation, final_cost = stepping_stone_method(optimal_allocation, costs)
        final_allocation_label = ttk.Label(result_frame, text="Final Allocation:", font=("Arial", 12, "bold"))
        final_allocation_label.grid(row=rows+7+rows*2, column=0, columnspan=cols+1, pady=(10, 5))

        for i in range(rows):
            for j in range(cols):
                allocation_value = final_allocation[i][j]
                cell_label = ttk.Label(result_frame, text=allocation_value, relief="solid", width=10, anchor="center")
                cell_label.grid(row=rows+8+rows*2+i, column=j, padx=5, pady=5)

        final_cost_label = ttk.Label(result_frame, text=f"Final Total Cost: {final_cost}", font=("Arial", 10))
        final_cost_label.grid(row=rows+8+rows*2+rows, column=0, columnspan=cols+1, pady=(5, 10))

        root.mainloop()

    except ValueError as e:
        messagebox.showerror("Error", f"Input Error: {str(e)}")

def steppingstone():
    window = tk.Tk()
    window.title("Transportation Problem Solver")

    # Outer border
    border_frame = tk.Frame(window, bg="#008080", bd=2)
    border_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Inner content inside the border
    inner_frame = ttk.Frame(border_frame, padding="10")
    inner_frame.pack(fill=tk.BOTH, expand=True)

    # Supply input
    supply_label = ttk.Label(inner_frame, text="Enter supply values (space separated):")
    supply_label.pack(pady=10)

    supply_entry = ttk.Entry(inner_frame, width=30)
    supply_entry.pack(pady=5)

    # Demand input
    demand_label = ttk.Label(inner_frame, text="Enter demand values (space separated):")
    demand_label.pack(pady=10)

    demand_entry = ttk.Entry(inner_frame, width=30)
    demand_entry.pack(pady=5)

    # Calculate button
    calculate_button = ttk.Button(inner_frame, text="Calculate", command=lambda: display_results(supply_entry, demand_entry))
    calculate_button.pack(pady=20)

    window.mainloop()

if __name__ == "__main__":
    steppingstone()
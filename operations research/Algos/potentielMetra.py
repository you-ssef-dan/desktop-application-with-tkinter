import random 
import tkinter as tk
from tkinter import ttk, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Generate task table for Potentiel Métra
def generate_task_table(num_tasks):
    task_table = []
    for i in range(num_tasks):
        duration = random.randint(1, 10)
        dependencies = random.sample(range(1, num_tasks + 1), random.randint(0, min(3, i)))
        dependencies = [dep for dep in dependencies if dep < i + 1]
        task_table.append({"id": i + 1, "duration": duration, "dependencies": dependencies})
    return task_table

# Potentiel Métra algorithm
def potentiel_metra(tasks):
    G = nx.DiGraph()

    # Add nodes and edges
    for task in tasks:
        G.add_node(task["id"], duration=task["duration"])
        for dep in task["dependencies"]:
            G.add_edge(dep, task["id"])

    # Add start and end nodes
    G.add_node(0, duration=0)
    G.add_node(len(tasks) + 1, duration=0)

    # Connect isolated nodes
    for task in tasks:
        if not list(G.predecessors(task["id"])):
            G.add_edge(0, task["id"])
        if not list(G.successors(task["id"])):
            G.add_edge(task["id"], len(tasks) + 1)

    # Earliest start times
    earliest_start = {}
    for node in nx.topological_sort(G):
        if node == 0:
            earliest_start[node] = 0
        else:
            pred_times = [earliest_start[pred] + G.nodes[pred]['duration'] for pred in G.predecessors(node)]
            earliest_start[node] = max(pred_times) if pred_times else 0

    # Latest start times
    latest_start = {}
    for node in reversed(list(nx.topological_sort(G))):
        if node == len(tasks) + 1:
            latest_start[node] = earliest_start[node]
        else:
            succ_times = [latest_start[succ] - G.nodes[node]['duration'] for succ in G.successors(node)]
            latest_start[node] = min(succ_times) if succ_times else earliest_start[node]

    # Calculate slack and identify critical path
    slack = {node: latest_start[node] - earliest_start[node] for node in G.nodes()}
    critical_path = [node for node, s in slack.items() if s == 0]

    return earliest_start, latest_start, slack, critical_path, G

# Display Potentiel Métra results
def display_potentiel_metra():
    try:
        # User input for number of tasks
        num_tasks = int(task_entry.get())
        tasks = generate_task_table(num_tasks)

        # Run Potentiel Métra
        earliest_start, latest_start, slack, critical_path, G = potentiel_metra(tasks)

        # Clear previous results
        for widget in result_frame.winfo_children():
            widget.destroy()

        # Display task details
        ttk.Label(result_frame, text="Tasks and Information:", font=("Arial", 12, "bold")).pack(pady=5)
        for task in tasks:
            task_info = f"Task {task['id']} (Duration: {task['duration']} | Dependencies: {task['dependencies']})"
            ttk.Label(result_frame, text=task_info).pack(anchor="w")

        # Display earliest and latest dates, slack, and critical path
        ttk.Label(result_frame, text="\nEarliest and Latest Dates:", font=("Arial", 12, "bold")).pack(pady=5)
        for node in G.nodes():
            node_info = f"Node {node}: Earliest={earliest_start[node]}, Latest={latest_start[node]}, Slack={slack[node]}"
            ttk.Label(result_frame, text=node_info).pack(anchor="w")

        ttk.Label(result_frame, text=f"\nCritical Path: {critical_path}", font=("Arial", 12, "bold")).pack(pady=5)

        # Visualize the graph
        def plot_graph():
            fig, ax = plt.subplots(figsize=(8, 6))
            pos = nx.spring_layout(G)
            labels = {node: f"{node}\nE={earliest_start[node]}" for node in G.nodes()}
            nx.draw(G, pos, with_labels=True, labels=labels, node_size=2000, node_color="lightblue", ax=ax)
            nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): f"{G.nodes[v]['duration']}" for u, v in G.edges()}, ax=ax)
            ax.set_title("Task Graph")

            # Embed the plot in the Tkinter window
            canvas = FigureCanvasTkAgg(fig, master=result_frame)
            canvas.draw()

            # Clear previous canvas if exists and replace with new one
            global current_canvas
            if current_canvas is not None:
                current_canvas.get_tk_widget().pack_forget()

            current_canvas = canvas
            current_canvas.get_tk_widget().pack(pady=10)

        plot_button = create_rounded_button(result_frame, "Visualize Graph", plot_graph)
        plot_button.pack(pady=10)

    except ValueError as e:
        messagebox.showerror("Error", f"Invalid Input: {str(e)}")

# Create rounded button
def create_rounded_button(master, text, command):
    canvas = tk.Canvas(master, width=150, height=40, bg="#F0F0F0", highlightthickness=0)
    rect = create_rounded_rectangle(canvas, 5, 5, 145, 35, radius=20, outline="#008080", width=2, fill="#E0F7FA")
    label = canvas.create_text(75, 20, text=text, font=("Arial", 10), fill="#008080")

    def on_click(event):
        command()

    def on_enter(event):
        canvas.itemconfig(rect, fill="#72BAA9")

    def on_leave(event):
        canvas.itemconfig(rect, fill="#E0F7FA")

    canvas.bind("<Button-1>", on_click)
    canvas.bind("<Enter>", on_enter)
    canvas.bind("<Leave>", on_leave)

    return canvas

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

# Main GUI
def PotentielMetra():
    window = tk.Tk()
    window.title("Potentiel Métra Method")

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

    # Task input
    global task_entry
    ttk.Label(scrollable_frame, text="Number of Tasks:").pack(pady=10)
    task_entry = ttk.Entry(scrollable_frame, width=20)
    task_entry.pack(pady=5)

    # Button for Potentiel Métra
    create_rounded_button(scrollable_frame, "Potentiel Métra", display_potentiel_metra).pack(pady=20)

    # Frame for results
    global result_frame, current_canvas
    result_frame = ttk.Frame(scrollable_frame, padding="10")
    result_frame.pack(fill="both", expand=True)
    current_canvas = None

    window.mainloop()

if __name__ == "__main__":
    PotentielMetra()

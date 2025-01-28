import networkx as nx
import matplotlib.pyplot as plt
import random
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Function to generate a directed graph
def generate_directed_graph(n):
    G = nx.DiGraph()
    for i in range(n):
        G.add_node(f"X{i}", size=800)
    for i in range(n):
        for j in range(i + 1, n):
            if random.choice([True, False]):
                weight = random.randint(1, 100)
                G.add_edge(f"X{i}", f"X{j}", weight=weight)
            else:
                weight = random.randint(1, 100)
                G.add_edge(f"X{j}", f"X{i}", weight=weight)
    return G

# Function to display the graph on a Tkinter canvas
def display_graph(G, canvas_frame, path=None):
    pos = nx.spring_layout(G, seed=42)
    node_sizes = [G.nodes[node]['size'] for node in G]
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_size=node_sizes, node_color="lightblue", font_weight="bold", arrows=True)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    if path:
        edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
        nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color='red', width=2, arrows=True)
    fig = plt.gcf()
    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Function to apply Bellman-Ford algorithm
def bellman_ford_graph(G, source, target):
    try:
        distance = nx.single_source_bellman_ford_path_length(G, source)
        path = nx.single_source_bellman_ford_path(G, source)[target]
        return path, distance[target]
    except nx.NetworkXNoPath:
        return None, None

# Main Tkinter window
def bellmanford():
    root = tk.Tk()
    root.title("Bellman-Ford Algorithm")

    # Create a scrollable frame
    main_frame = ttk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)
    canvas = tk.Canvas(main_frame)
    scroll_y = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
    scroll_x = ttk.Scrollbar(main_frame, orient=tk.HORIZONTAL, command=canvas.xview)
    scrollable_frame = ttk.Frame(canvas)
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
    scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

    # Input frame
    input_frame = ttk.Frame(scrollable_frame)
    input_frame.pack(pady=10)
    ttk.Label(input_frame, text="Number of nodes:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
    num_nodes_entry = ttk.Entry(input_frame, width=10, font=("Arial", 12))
    num_nodes_entry.grid(row=0, column=1, padx=5, pady=5)
    ttk.Label(input_frame, text="Start node (e.g., X0...XN):", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5)
    start_node_entry = ttk.Entry(input_frame, width=10, font=("Arial", 12))
    start_node_entry.grid(row=1, column=1, padx=5, pady=5)
    ttk.Label(input_frame, text="Target node (e.g., X0...XN):", font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=5)
    target_node_entry = ttk.Entry(input_frame, width=10, font=("Arial", 12))
    target_node_entry.grid(row=2, column=1, padx=5, pady=5)

    # Create rounded button
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
        canvas.tag_bind(label, "<Button-1>", on_click)
        canvas.tag_bind(label, "<Enter>", on_enter)
        canvas.tag_bind(label, "<Leave>", on_leave)

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

    # Execute button
    create_rounded_button(scrollable_frame, "Execute", lambda: execute_bellmanford()).pack(pady=10)

    # Result frame
    result_frame = ttk.Frame(scrollable_frame)
    result_frame.pack(pady=10)
    result_label = ttk.Label(result_frame, text="", font=("Arial", 12), justify="left")
    result_label.pack()

    # Canvas frame for graph display (at the bottom)
    canvas_frame = ttk.Frame(scrollable_frame)
    canvas_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    # Execute button function
    def execute_bellmanford():
        try:
            num_nodes = int(num_nodes_entry.get())
            start_node = start_node_entry.get()
            target_node = target_node_entry.get()
            if not (start_node and target_node and start_node.startswith("X") and target_node.startswith("X")):
                raise ValueError("Invalid start or target node.")
            G = generate_directed_graph(num_nodes)
            path, distance = bellman_ford_graph(G, start_node, target_node)
            # Clear the canvas and render the new graph
            for widget in canvas_frame.winfo_children():
                widget.destroy()
            display_graph(G, canvas_frame, path)
            if path:
                result_label.config(
                    text=f"Distance from {start_node} to {target_node}: {distance}\nPath: {' -> '.join(path)}"
                )
            else:
                result_label.config(text=f"No path from {start_node} to {target_node}.")
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    root.mainloop()

if __name__ == "__main__":
    bellmanford()
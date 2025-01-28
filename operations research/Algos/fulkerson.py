import random
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Function to generate a random graph
def generate_random_graph(num_vertices, max_capacity=10):
    G = nx.DiGraph()  # Create a directed graph
    for i in range(num_vertices):
        for j in range(num_vertices):
            if i != j:  # No self-loops
                capacity = random.randint(1, max_capacity)  # Random capacities
                G.add_edge(i, j, capacity=capacity)
    return G

# Breadth-first search for augmenting path
def bfs(capacity, flow, source, sink):
    parent = [-1] * len(capacity)
    parent[source] = -2
    queue = deque([(source, float('inf'))])
    while queue:
        u, min_cap = queue.popleft()
        for v in range(len(capacity)):
            if parent[v] == -1 and capacity[u][v] - flow[u][v] > 0:
                parent[v] = u
                new_flow = min(min_cap, capacity[u][v] - flow[u][v])
                if v == sink:
                    return new_flow, parent
                queue.append((v, new_flow))
    return 0, parent

# Ford-Fulkerson algorithm for max flow
def ford_fulkerson(capacity, source, sink):
    n = len(capacity)
    flow = [[0] * n for _ in range(n)]
    max_flow = 0
    while True:
        path_flow, parent = bfs(capacity, flow, source, sink)
        if path_flow == 0:
            break
        max_flow += path_flow
        v = sink
        while v != source:
            u = parent[v]
            flow[u][v] += path_flow
            flow[v][u] -= path_flow
            v = u
    return max_flow, flow

# Find minimum cut using BFS
def find_min_cut(capacity, flow, source):
    visited = [False] * len(capacity)
    queue = deque([source])
    visited[source] = True
    while queue:
        u = queue.popleft()
        for v in range(len(capacity)):
            if capacity[u][v] - flow[u][v] > 0 and not visited[v]:
                visited[v] = True
                queue.append(v)
    return visited

# Draw graph with min cut
def draw_graph_with_cut(G, min_cut):
    pos = nx.spring_layout(G)
    plt.figure(figsize=(8, 8))
    edges = G.edges()
    edge_colors = ['red' if min_cut[u] and not min_cut[v] else 'black' for u, v in edges]
    node_colors = ['green' if min_cut[u] else 'blue' for u in G.nodes()]
    nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color=edge_colors, 
            node_size=500, font_size=16, font_weight='bold')
    plt.show()

# Main program using Tkinter
def fulkerson():
    root = tk.Tk()
    root.title("Ford-Fulkerson Algorithm")

    # Outer frame for border
    outer_frame = tk.Frame(root, bg="#008080", bd=5)
    outer_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Create a canvas and a scrollbar
    canvas = tk.Canvas(outer_frame)
    scrollbar = tk.Scrollbar(outer_frame, orient="vertical", command=canvas.yview)
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

    ttk.Label(input_frame, text="Enter the number of vertices:", font=("Arial", 14)).pack(side=tk.LEFT, padx=5)
    num_vertices_entry = ttk.Entry(input_frame, width=10, font=("Arial", 14))
    num_vertices_entry.pack(side=tk.LEFT, padx=5)

    def run_algorithm():
        try:
            num_vertices = int(num_vertices_entry.get())
            if num_vertices < 2:
                raise ValueError("The number of vertices must be at least 2.")
            
            # Generate the graph
            G = generate_random_graph(num_vertices)
            
            # Define source and sink
            source = 0
            sink = num_vertices - 1
            
            # Create capacity matrix
            capacity = [[0] * num_vertices for _ in range(num_vertices)]
            for u, v, data in G.edges(data=True):
                capacity[u][v] = data['capacity']
            
            # Calculate max flow
            max_flow, flow = ford_fulkerson(capacity, source, sink)
            
            # Find minimum cut
            min_cut = find_min_cut(capacity, flow, source)
            
            # Clear previous results (destroy previous graph if exists)
            if hasattr(run_algorithm, 'canvas_graph'):
                run_algorithm.canvas_graph.get_tk_widget().destroy()
            
            # Show results in a message box
            result_label.config(text=f"Maximum Flow: {max_flow}")
            
            # Draw the graph with the min cut
            fig = plt.figure(figsize=(8, 8))
            pos = nx.spring_layout(G)
            edges = G.edges()
            edge_colors = ['red' if min_cut[u] and not min_cut[v] else 'black' for u, v in edges]
            node_colors = ['green' if min_cut[u] else 'blue' for u in G.nodes()]
            nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color=edge_colors, 
                    node_size=500, font_size=16, font_weight='bold')
            
            run_algorithm.canvas_graph = FigureCanvasTkAgg(fig, master=scrollable_frame)
            run_algorithm.canvas_graph.draw()
            run_algorithm.canvas_graph.get_tk_widget().pack()

        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))

    # Create rounded button
    def create_rounded_button(master, text, command):
        canvas_button = tk.Canvas(master, width=150, height=40, bg="#F0F0F0", highlightthickness=0)
        rect_button = create_rounded_rectangle(canvas_button, 5, 5, 145, 35, radius=20, outline="#008080", width=2, fill="#E0F7FA")
        label_button = canvas_button.create_text(75, 20, text=text, font=("Arial", 10), fill="#008080")

        def on_click(event):
            command()

        def on_enter(event):
            canvas_button.itemconfig(rect_button, fill="#72BAA9")  # Coral color for hover

        def on_leave(event):
            canvas_button.itemconfig(rect_button, fill="#E0F7FA")  # Light blue color for default

        canvas_button.bind("<Button-1>", on_click)
        canvas_button.bind("<Enter>", on_enter)
        canvas_button.bind("<Leave>", on_leave)
        canvas_button.tag_bind(label_button, "<Button-1>", on_click)
        canvas_button.tag_bind(label_button, "<Enter>", on_enter)
        canvas_button.tag_bind(label_button, "<Leave>", on_leave)

        return canvas_button

    # Create rounded rectangle
    def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=25, **kwargs):
        points = [
            x1 + radius, y1,
            x1 + radius, y1,
            x2 - radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1,
        ]
        return canvas.create_polygon(points, **kwargs, smooth=True)

    # Button to run the algorithm
    create_rounded_button(scrollable_frame, "Run Algorithm", run_algorithm).pack(pady=20)

    # Label to display results
    result_label = ttk.Label(scrollable_frame, text="", font=("Arial", 12))
    result_label.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    fulkerson()
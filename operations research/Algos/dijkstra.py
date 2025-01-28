import matplotlib.pyplot as plt
import networkx as nx
import random
import heapq
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Function to generate an undirected graph with random weights
def generate_graph(num_nodes, max_weight=100):
    graph = nx.Graph()
    nodes = [f"X{i+1}" for i in range(num_nodes)]
    graph.add_nodes_from(nodes)

    # Randomly add edges with weights between nodes
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            weight = random.randint(1, max_weight)
            graph.add_edge(nodes[i], nodes[j], weight=weight)
    
    return graph

# Standard Dijkstra's algorithm function
def dijkstra(graph, start_node):
    priority_queue = [(0, start_node)]  # (distance, node)
    distances = {node: float('inf') for node in graph.nodes()}
    distances[start_node] = 0
    paths = {node: [] for node in graph.nodes()}
    paths[start_node] = [start_node]
    visited = set()
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        # Skip if already visited
        if current_node in visited:
            continue
        
        # Mark the node as visited
        visited.add(current_node)

        # Check all neighbors of the current node
        for neighbor in graph.neighbors(current_node):
            edge_weight = graph[current_node][neighbor]['weight']
            new_distance = current_distance + edge_weight
            
            # Update distances and path if a shorter path is found
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                paths[neighbor] = paths[current_node] + [neighbor]
                heapq.heappush(priority_queue, (new_distance, neighbor))

    return distances, paths

# Function to plot the graph with shortest paths highlighted
def plot_graph(graph, paths, start_node, title):
    pos = nx.spring_layout(graph, seed=42)
    
    # Identify edges in the shortest paths and color them red
    edges_in_paths = [(u, v) for path in paths.values() for u, v in zip(path, path[1:])]
    edge_colors = ['red' if (u, v) in edges_in_paths or (v, u) in edges_in_paths else 'black' for u, v in graph.edges()]

    node_colors = ['lightblue' if n == start_node else 'lightgrey' for n in graph.nodes()]
    
    plt.figure(figsize=(10, 6))
    nx.draw(graph, pos, with_labels=True, node_color=node_colors, edge_color=edge_colors, node_size=500, font_size=10)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels={(u, v): f"{d['weight']}" for u, v, d in graph.edges(data=True)})

    plt.title(title)
    return plt.gcf()

# Function to display the shortest paths and their weights
def display_paths_table(distances, paths):
    result = "\nShortest Paths from Start Node:\n"
    result += f"{'Destination':<12}{'Path Weight':<10}{'Path'}\n"
    result += "="*40 + "\n"
    for dest, distance in distances.items():
        result += f"{dest:<12}{distance:<10}{' -> '.join(paths[dest])}\n"
    return result

# Main program
def mainDijkstra():
    root = tk.Tk()
    root.title("Dijkstra's Algorithm")
    root.geometry("800x600")  # Set the window size

    # Outer frame for the colored border
    border_frame = tk.Frame(root, bg="#008080", width=800, height=600)
    border_frame.pack(padx=10, pady=10, fill="both", expand=True)

    # Inner frame for the content
    content_frame = ttk.Frame(border_frame)
    content_frame.pack(padx=5, pady=5, fill="both", expand=True)

    # Create a scrollable frame inside the content frame
    canvas = tk.Canvas(content_frame)
    scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Input frame for user entries
    input_frame = ttk.Frame(scrollable_frame)
    input_frame.pack(pady=10)

    ttk.Label(input_frame, text="Enter the number of nodes:", font=("Arial", 14)).pack(side=tk.LEFT, padx=5)
    num_nodes_entry = ttk.Entry(input_frame, width=10, font=("Arial", 14))
    num_nodes_entry.pack(side=tk.LEFT, padx=5)

    ttk.Label(input_frame, text="Enter the starting node (e.g: X1...XN):", font=("Arial", 14)).pack(side=tk.LEFT, padx=5)
    start_node_entry = ttk.Entry(input_frame, width=10, font=("Arial", 14))
    start_node_entry.pack(side=tk.LEFT, padx=5)

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

    # Button frame for the Execute button
    button_frame = ttk.Frame(scrollable_frame)
    button_frame.pack(pady=10)

    create_rounded_button(button_frame, "Execute", lambda: execute_dijkstra()).pack()

    # Frame for graph and results (below the button frame)
    graph_frame = ttk.Frame(scrollable_frame)
    graph_frame.pack(pady=20, fill=tk.BOTH, expand=True)

    result_label = ttk.Label(graph_frame, text="", font=("Arial", 12), justify="left")
    result_label.pack(pady=10)

    canvas_graph = None

    # Function to execute the algorithm and render the graph and paths
    def execute_dijkstra():
        nonlocal canvas_graph

        try:
            num_nodes = int(num_nodes_entry.get())
            start_node = start_node_entry.get()
            if not start_node.startswith("X") or not start_node[1:].isdigit() or int(start_node[1:]) > num_nodes:
                raise ValueError("Invalid starting node.")
            
            graph = generate_graph(num_nodes)
            distances, paths = dijkstra(graph, start_node)

            # Plot and render the graph
            fig = plot_graph(graph, paths, start_node, title="Graph with Shortest Paths Highlighted")

            if canvas_graph:
                canvas_graph.get_tk_widget().destroy()

            canvas_graph = FigureCanvasTkAgg(fig, master=graph_frame)
            canvas_graph.draw()
            canvas_graph.get_tk_widget().pack()

            result = display_paths_table(distances, paths)
            result_label.config(text=result)
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    root.mainloop()

if __name__ == "__main__":
    mainDijkstra()
import networkx as nx
import matplotlib.pyplot as plt
import random
from matplotlib import colors as mcolors
import time
import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Function to generate a random graph
def generate_random_graph(x):
    G = nx.Graph()
    G.add_nodes_from(range(x))
    for i in range(x):
        for j in range(i + 1, x):
            if random.random() < 0.5:  # 50% probability to add an edge
                G.add_edge(i, j)
    return G


def on_enter(event, canvas, rect):
    canvas.itemconfig(rect, fill="#72BAA9")  # Coral color for hover


def on_leave(event, canvas, rect):
    canvas.itemconfig(rect, fill="#E0F7FA")  # Light blue color for default


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


# Welsh-Powell algorithm for graph coloring
def welsh_powell_algorithm(G):
    nodes_sorted = sorted(G.nodes(), key=lambda x: G.degree(x), reverse=True)
    coloring = {}
    current_color = 0

    for node in nodes_sorted:
        if node not in coloring:
            neighbor_colors = {coloring[neighbor] for neighbor in G.neighbors(node) if neighbor in coloring}
            for color in range(current_color + 1):
                if color not in neighbor_colors:
                    coloring[node] = color
                    break
            else:
                current_color += 1
                coloring[node] = current_color

    return coloring


# Function to draw the colored graph
def draw_colored_graph(G, coloring, canvas_frame):
    colors_list = list(mcolors.CSS4_COLORS.values())
    unique_colors = random.sample(colors_list, max(coloring.values()) + 1)
    colors = [unique_colors[coloring[node]] for node in G.nodes()]

    # Create a Matplotlib figure
    fig, ax = plt.subplots(figsize=(5, 5))
    nx.draw(G, ax=ax, with_labels=True, node_color=colors, node_size=500, font_size=10)

    # Embed the figure in the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)
    canvas.draw()


# Main execution
def welshpowel():
    def on_submit():
        user_input = entry.get()
        if user_input.isdigit():
            x = int(user_input)

            # Clear the canvas frame before drawing a new graph
            for widget in canvas_frame.winfo_children():
                widget.destroy()

            # Measure the total execution time
            start_time = time.time()

            random_graph = generate_random_graph(x)
            coloring = welsh_powell_algorithm(random_graph)

            # Display the number of colors used
            num_colors = max(coloring.values()) + 1
            result_label.config(text=f"Chromatic number is: {num_colors}")

            # Draw the colored graph
            draw_colored_graph(random_graph, coloring, canvas_frame)

            # Calculate the total execution time
            end_time = time.time()
            total_time = end_time - start_time

            # Display the total execution time
            time_label.config(text=f"Total execution time: {total_time:.4f} seconds")
        else:
            messagebox.showwarning("Input Error", "Please enter a valid number.")

    # Create a Tkinter root window
    root = tk.Tk()
    root.title("Welsh-Powell Algorithm")

    # Outer border
    border_frame = tk.Frame(root, bg="#008080", bd=1)
    border_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=False)

    # Inner frame
    inner_frame = tk.Frame(border_frame, bg="#F0F0F0")
    inner_frame.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

    # Input frame
    input_frame = tk.Frame(inner_frame, bg="#F0F0F0")
    input_frame.pack(pady=10)

    tk.Label(input_frame, text="Enter the number of vertices:", bg="#F0F0F0").grid(row=0, column=0, pady=5, padx=5)
    entry = tk.Entry(input_frame)
    entry.grid(row=0, column=1, pady=5, padx=5)

    # Styled Submit Button
    canvas = tk.Canvas(input_frame, width=150, height=50, bg="#F0F0F0", highlightthickness=0)
    canvas.grid(row=1, column=0, columnspan=2, pady=10)

    rect = create_rounded_rectangle(canvas, 10, 10, 140, 40, radius=20, fill="#E0F7FA", outline="#008080", width=2)
    label = canvas.create_text(75, 25, text="Submit", font=("Arial", 10), fill="#008080")

    def on_click(event):
        on_submit()

    # Bind click and hover events
    canvas.tag_bind(rect, "<Button-1>", on_click)
    canvas.tag_bind(label, "<Button-1>", on_click)
    canvas.tag_bind(rect, "<Enter>", lambda event: on_enter(event, canvas, rect))
    canvas.tag_bind(rect, "<Leave>", lambda event: on_leave(event, canvas, rect))
    canvas.tag_bind(label, "<Enter>", lambda event: on_enter(event, canvas, rect))
    canvas.tag_bind(label, "<Leave>", lambda event: on_leave(event, canvas, rect))

    # Result labels
    result_label = tk.Label(inner_frame, text="", bg="#F0F0F0", font=("Arial", 10))
    result_label.pack(pady=5)
    time_label = tk.Label(inner_frame, text="", bg="#F0F0F0", font=("Arial", 10))
    time_label.pack(pady=5)

    # Canvas frame for the graph
    canvas_frame = tk.Frame(inner_frame, bg="#F0F0F0")
    canvas_frame.pack(fill=tk.BOTH, expand=True, pady=10)

    root.mainloop()


if __name__ == "__main__":
    welshpowel()

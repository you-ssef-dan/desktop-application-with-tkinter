import tkinter as tk

from Algos.fulkerson import fulkerson
from Algos.welshPowel import welshpowel
from Algos.dijkstra import mainDijkstra
from Algos.bellmanFord import bellmanford
from Algos.steppingStone import steppingstone
from Algos.potentielMetra import PotentielMetra
from Algos.moindreCout import leastCostMethod
from Algos.nordWest import nordWest
from Algos.kruskal import kruskal


def on_box_click(label):
    # Define the algorithm functions here
    if label == "Welsh Powel":
        welshpowel()
        #subprocess.run(["python", "main.py"]) 
        # Call the Welsh-Powell algorithm here
    elif label == "Dijkstra":
        mainDijkstra()
        # Call the Dijkstra algorithm here
    elif label == "Kruskal":
        kruskal()
        # Call the Kruskal algorithm here
    elif label == "Bellman Ford":
        bellmanford()
        # Call the Bellman Ford algorithm here
    elif label == "Nord-Ouest":
        nordWest()
        # Call the Nord-Ouest algorithm here
    elif label == "stepping stone":
        steppingstone()
        # Call the stepping stone algorithm here
    elif label == "Ford Fulkerson":
        fulkerson()
        # Call the Ford Fulkerson algorithm here
    elif label == "Moindre Cout":
        leastCostMethod()
        # Call the Moindre Cout algorithm here
    elif label == "Potentiel Metra":
        PotentielMetra()
        # Call the Potentiel Metra algorithm here

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


def render_algorithmes_page(canvas):
    # Clear existing canvas content
    canvas.delete("all")

    # Draw the outer border (expanded height to fit all boxes)
    canvas.create_rectangle(50, 50, 550, 400, outline="#008080", width=2)  # Increased height

    # Add boxes for algorithms
    boxes = [
        (100, 100, 250, 140, "Welsh Powel"),
        (300, 100, 450, 140, "Dijkstra"),
        (100, 160, 250, 200, "Kruskal"),
        (300, 160, 450, 200, "Bellman Ford"),
        (100, 220, 250, 260, "Nord-Ouest"),
        (300, 220, 450, 260, "Moindre Cout"),
        (100, 280, 250, 320, "Ford Fulkerson"),
        (300, 280, 450, 320, "stepping stone"),
        (175, 340, 375, 380, "Potentiel Metra"),
    ]

    for x1, y1, x2, y2, text in boxes:
        rect = create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=20, outline="#008080", width=2, fill="#E0F7FA")
        label = canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=text, font=("Arial", 10), fill="#008080")

        # Bind click event to each rectangle and label
        def on_click(event, t=text):
            on_box_click(t)

        canvas.tag_bind(rect, "<Button-1>", on_click)
        canvas.tag_bind(label, "<Button-1>", on_click)

        # Bind hover events to each rectangle
        canvas.tag_bind(rect, "<Enter>", lambda event, c=canvas, r=rect: on_enter(event, c, r))
        canvas.tag_bind(rect, "<Leave>", lambda event, c=canvas, r=rect: on_leave(event, c, r))
        canvas.tag_bind(label, "<Enter>", lambda event, c=canvas, r=rect: on_enter(event, c, r))
        canvas.tag_bind(label, "<Leave>", lambda event, c=canvas, r=rect: on_leave(event, c, r))


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Interface Graphique Tkinter GUI")

    # Set the canvas dimensions
    canvas = tk.Canvas(root, width=600, height=400, bg="#F0F0F0")  # Light grey background
    canvas.pack()

    render_algorithmes_page(canvas)

    root.mainloop()
import string  # To manipulate strings
import random  # To generate random values
import time  # To measure execution time
import matplotlib.pyplot as plt  # To plot graphs
import networkx as nx  # To create and visualize graphs
import tkinter as tk
from tkinter import ttk  # Import ttk for styling
from tkinter import messagebox  # For displaying alerts
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Function to create node labels (A, B, ..., Z, AA, AB, ..., ZZ)
def creer_labels_noeuds(nombre_noeuds):
    lettres = string.ascii_uppercase
    labels = []
    for i in range(nombre_noeuds):
        label = ""
        while i >= 0:
            label = lettres[i % 26] + label
            i = i // 26 - 1
        labels.append(label)
    return labels

# Function to create a graph with random weights between 1 and 99
def creer_graphe(nombre_noeuds):
    noeuds = creer_labels_noeuds(nombre_noeuds)
    liens = []
    for i in range(nombre_noeuds):
        for j in range(i + 1, nombre_noeuds):
            poids = random.randint(1, 99)
            liens.append((noeuds[i], noeuds[j], poids))
    return noeuds, liens

# Class to manage disjoint sets (Union-Find)
class GestionEnsemble:
    def __init__(self, nombre_noeuds):
        self.parent = list(range(nombre_noeuds))
        self.hauteur = [0] * nombre_noeuds

    def trouver_chef(self, noeud):
        if self.parent[noeud] != noeud:
            self.parent[noeud] = self.trouver_chef(self.parent[noeud])
        return self.parent[noeud]

    def fusionner(self, noeud1, noeud2):
        chef1 = self.trouver_chef(noeud1)
        chef2 = self.trouver_chef(noeud2)
        if chef1 != chef2:
            if self.hauteur[chef1] > self.hauteur[chef2]:
                self.parent[chef2] = chef1
            elif self.hauteur[chef1] < self.hauteur[chef2]:
                self.parent[chef1] = chef2
            else:
                self.parent[chef2] = chef1
                self.hauteur[chef1] += 1

# Kruskal's algorithm to find the minimum spanning tree
def algorithme_kruskal(noeuds, liens):
    liens_tries = sorted(liens, key=lambda x: x[2])
    gestion_ensemble = GestionEnsemble(len(noeuds))
    acm = []
    cout_total = 0

    for lien in liens_tries:
        noeud1, noeud2, poids = lien
        index1 = noeuds.index(noeud1)
        index2 = noeuds.index(noeud2)
        if gestion_ensemble.trouver_chef(index1) != gestion_ensemble.trouver_chef(index2):
            gestion_ensemble.fusionner(index1, index2)
            acm.append(lien)
            cout_total += poids
        if len(acm) == len(noeuds) - 1:
            break

    return acm, cout_total

# Function to display the graph with NetworkX
def afficher_graphe(noeuds, liens, acm=None, titre="Graph"):
    G = nx.Graph()
    for noeud1, noeud2, poids in liens:
        G.add_edge(noeud1, noeud2, weight=poids)
    positions = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(10, 7))
    nx.draw(G, positions, with_labels=True, node_color='lightblue', node_size=500, font_size=10,
            font_weight='bold', edge_color='gray')
    nx.draw_networkx_edge_labels(G, positions, edge_labels={(noeud1, noeud2): f'{poids}' for noeud1, noeud2, poids in liens})
    if acm:
        liens_acm = [(noeud1, noeud2) for noeud1, noeud2, _ in acm]
        nx.draw_networkx_edges(G, positions, edgelist=liens_acm, width=3, edge_color='blue')
    plt.title(titre)
    return plt.gcf()

# Function to create a rounded rectangle
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
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1,
    ]
    return canvas.create_polygon(points, **kwargs, smooth=True)

# Main function to run the program
def kruskal():
    root = tk.Tk()
    root.title("Kruskal's Algorithm")

    # Outer border for the entire window
    outer_frame = tk.Frame(root, bg="#008080", bd=5)  # Outer border with desired color and width
    outer_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Create a canvas and a scrollbar inside the outer frame
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

    # Label for the input
    ttk.Label(input_frame, text="Enter the number of nodes:", font=("Arial", 14, "bold")).pack(side=tk.LEFT, padx=5)

    # Create a text input field
    nombre_noeuds_entry = ttk.Entry(input_frame, font=("Arial", 14), width=10)
    nombre_noeuds_entry.pack(side=tk.LEFT, padx=5)
    nombre_noeuds_entry.insert(0, "5")  # Default value

    def on_enter(e):
        e.widget.itemconfig(e.widget.find_withtag("rect"), fill='#00cccc')

    def on_leave(e):
        e.widget.itemconfig(e.widget.find_withtag("rect"), fill='#E0F7FA')

    def executer_kruskal():
        try:
            nombre_noeuds = int(nombre_noeuds_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")
            return
        
        debut = time.time()
        noeuds, liens = creer_graphe(nombre_noeuds)
        fig = afficher_graphe(noeuds, liens, titre="Original Graph")
        acm, cout_total = algorithme_kruskal(noeuds, liens)
        fig_acm = afficher_graphe(noeuds, liens, acm, titre="Graph with MST")
        fin = time.time()
        temps_execution = fin - debut
        resultats_text.set(f"Total cost of MST: {cout_total} euros\nExecution time: {temps_execution:.4f} seconds")

        # Check if there's an existing canvas, and destroy it if it exists
        if hasattr(executer_kruskal, 'canvas'):
            executer_kruskal.canvas.get_tk_widget().destroy()

        # Create a new canvas with the updated graph
        executer_kruskal.canvas = FigureCanvasTkAgg(fig_acm, master=scrollable_frame)
        executer_kruskal.canvas.draw()
        executer_kruskal.canvas.get_tk_widget().pack()

    # Canvas for rounded button
    button_canvas = tk.Canvas(scrollable_frame, width=120, height=50)
    button_canvas.pack(pady=10)
    button_rect = create_rounded_rectangle(button_canvas, 5, 5, 115, 45, radius=20, fill='#008080', outline='')
    button_canvas.create_text(60, 25, text="Execute", fill='white', font=('Helvetica', 12, 'bold'))
    button_canvas.bind("<Button-1>", lambda e: executer_kruskal())
    button_canvas.bind("<Enter>", lambda e: button_canvas.itemconfig(button_rect, fill='#00cccc'))
    button_canvas.bind("<Leave>", lambda e: button_canvas.itemconfig(button_rect, fill='#008080'))

    # This will now be placed under the button
    resultats_text = tk.StringVar()

    # Create label for results, placed below the button
    resultats_label = tk.Label(scrollable_frame, textvariable=resultats_text, font=("Arial", 12))
    resultats_label.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    kruskal()

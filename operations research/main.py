import tkinter as tk
from PIL import Image, ImageTk, ImageOps
import sys
import os
from algos import render_algorithmes_page

def resource_path(relative_path):
    """Get the absolute path to a resource, works for dev and PyInstaller."""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        # Running in development mode
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def on_button_click(label, canvas, root):
    if label == "Enter":
        render_algorithmes_page(canvas)
    elif label == "Exit":
        show_custom_dialog(root)
    else:
        print(f"You clicked on {label}!")

def show_custom_dialog(root):
    dialog = tk.Toplevel(root)
    dialog.title("Confirmation")
    dialog.geometry("300x150")
    dialog.configure(bg="#F0F0F0")

    canvas = tk.Canvas(dialog, width=300, height=150, bg="#F0F0F0")
    canvas.pack()

    canvas.create_rectangle(10, 10, 290, 140, outline="#008080", width=2)
    canvas.create_text(150, 40, text="Are you sure you want to exit?", font=("Arial", 12), fill="#008080")

    def on_yes():
        root.quit()

    def on_no():
        dialog.destroy()

    rect_yes = create_rounded_rectangle(canvas, 50, 80, 120, 110, radius=10, outline="#008080", width=2, fill="#E0F7FA")
    label_yes = canvas.create_text(85, 95, text="Yes", font=("Arial", 10), fill="#008080")

    rect_no = create_rounded_rectangle(canvas, 180, 80, 250, 110, radius=10, outline="#008080", width=2, fill="#E0F7FA")
    label_no = canvas.create_text(215, 95, text="No", font=("Arial", 10), fill="#008080")

    canvas.tag_bind(rect_yes, "<Button-1>", lambda event: on_yes())
    canvas.tag_bind(label_yes, "<Button-1>", lambda event: on_yes())

    canvas.tag_bind(rect_no, "<Button-1>", lambda event: on_no())
    canvas.tag_bind(label_no, "<Button-1>", lambda event: on_no())

    canvas.tag_bind(rect_yes, "<Enter>", lambda event: on_enter(event, canvas, rect_yes))
    canvas.tag_bind(rect_yes, "<Leave>", lambda event: on_leave(event, canvas, rect_yes))
    canvas.tag_bind(label_yes, "<Enter>", lambda event: on_enter(event, canvas, rect_yes))
    canvas.tag_bind(label_yes, "<Leave>", lambda event: on_leave(event, canvas, rect_yes))

    canvas.tag_bind(rect_no, "<Enter>", lambda event: on_enter(event, canvas, rect_no))
    canvas.tag_bind(rect_no, "<Leave>", lambda event: on_leave(event, canvas, rect_no))
    canvas.tag_bind(label_no, "<Enter>", lambda event: on_enter(event, canvas, rect_no))
    canvas.tag_bind(label_no, "<Leave>", lambda event: on_leave(event, canvas, rect_no))

def on_enter(event, canvas, rect):
    canvas.itemconfig(rect, fill="#72BAA9")

def on_leave(event, canvas, rect):
    canvas.itemconfig(rect, fill="#E0F7FA")

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

def create_interface():
    root = tk.Tk()
    root.title("Graphical Interface Tkinter GUI")

    # Create a canvas
    canvas = tk.Canvas(root, width=600, height=600, bg="#F0F0F0")
    canvas.pack()

    # Draw the outer border
    canvas.create_rectangle(40, 45, 580, 530, outline="#008080", width=2)

    # Load and resize the EMSI logo (left top)
    try:
        logo_path = resource_path("image.png")
        logo = Image.open(logo_path)
        logo = logo.resize((250, 80), Image.Resampling.LANCZOS)

        # Add a background color that matches the window's background
        bg_color = "#F0F0F0"
        logo_with_bg = ImageOps.expand(logo, border=10, fill=bg_color)
        logo_tk = ImageTk.PhotoImage(logo_with_bg)

        # Store the image as a global reference to prevent garbage collection
        canvas.logo_image = logo_tk

        # Add the logo to the top-left
        canvas.create_image(50, 50, image=logo_tk, anchor="nw")
    except Exception as e:
        print(f"Could not load logo: {e}")
        # Create a text placeholder if image loading fails
        canvas.create_text(50, 50, text="EMSI", font=("Arial", 20, "bold"), fill="#008080", anchor="nw")

    # Load and resize the second image (right top)
    try:
        tk_logo_path = resource_path("tkinter.png")
        tk_logo = Image.open(tk_logo_path)
        tk_logo = tk_logo.resize((180, 80), Image.Resampling.LANCZOS)

        # Add a background color that matches the window's background
        tk_logo_with_bg = ImageOps.expand(tk_logo, border=10, fill=bg_color)
        tk_logo_tk = ImageTk.PhotoImage(tk_logo_with_bg)

        # Store the image as a global reference to prevent garbage collection
        canvas.tk_logo_image = tk_logo_tk

        # Add the second image to the top-right
        canvas.create_image(550, 50, image=tk_logo_tk, anchor="ne")
    except Exception as e:
        print(f"Could not load tk logo: {e}")
        # Create a text placeholder if image loading fails
        canvas.create_text(550, 50, text="TK", font=("Arial", 20, "bold"), fill="#008080", anchor="ne")

    # Add labels inside the inner rectangle
    canvas.create_text(300, 220, text="Operational Research Algorithm", font=("Arial", 18), fill="#008080")

    # Add "Created by:" and "Supervised by:" text below the logo
    canvas.create_text(170, 300, text="Created by:", font=("Arial", 12, "bold"), fill="#008080")
    canvas.create_text(170, 325, text="YOUSSEF DANOUN", font=("Arial", 10), fill="#008080")

    canvas.create_text(450, 300, text="Supervised by:", font=("Arial", 12, "bold"), fill="#008080")
    canvas.create_text(450, 325, text="DR.EL MKHALET MOUNA", font=("Arial", 10), fill="#008080")

    # Create rounded rectangles for "Enter" and "Exit"
    rect1 = create_rounded_rectangle(canvas, 170, 380, 270, 410, radius=20, outline="#008080", width=2, fill="#E0F7FA")
    label1 = canvas.create_text(220, 395, text="Enter", font=("Arial", 10), fill="#008080")

    rect2 = create_rounded_rectangle(canvas, 350, 380, 450, 410, radius=20, outline="#008080", width=2, fill="#E0F7FA")
    label2 = canvas.create_text(400, 395, text="Exit", font=("Arial", 10), fill="#008080")

    # Add "Academic Year 2024/2025" lower below the buttons
    canvas.create_text(300, 470, text="Academic Year 2024/2025", font=("Arial", 12, "italic"), fill="#008080")

    # Bind click events
    def on_click(event, t, r):
        on_button_click(t, canvas, root)
        canvas.itemconfig(r, fill="#4CAF50")

    canvas.tag_bind(rect1, "<Button-1>", lambda event: on_click(event, "Enter", rect1))
    canvas.tag_bind(label1, "<Button-1>", lambda event: on_click(event, "Enter", rect1))

    canvas.tag_bind(rect2, "<Button-1>", lambda event: on_click(event, "Exit", rect2))
    canvas.tag_bind(label2, "<Button-1>", lambda event: on_click(event, "Exit", rect2))

    # Bind hover events
    canvas.tag_bind(rect1, "<Enter>", lambda event: on_enter(event, canvas, rect1))
    canvas.tag_bind(rect1, "<Leave>", lambda event: on_leave(event, canvas, rect1))
    canvas.tag_bind(label1, "<Enter>", lambda event: on_enter(event, canvas, rect1))
    canvas.tag_bind(label1, "<Leave>", lambda event: on_leave(event, canvas, rect1))

    canvas.tag_bind(rect2, "<Enter>", lambda event: on_enter(event, canvas, rect2))
    canvas.tag_bind(rect2, "<Leave>", lambda event: on_leave(event, canvas, rect2))
    canvas.tag_bind(label2, "<Enter>", lambda event: on_enter(event, canvas, rect2))
    canvas.tag_bind(label2, "<Leave>", lambda event: on_leave(event, canvas, rect2))

    root.mainloop()


if __name__ == "__main__":
    create_interface()

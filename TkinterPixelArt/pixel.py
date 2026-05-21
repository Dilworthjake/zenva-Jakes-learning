from tkinter import *
import tkinter as tk
import tkinter.colorchooser as colorchooser
from PIL import ImageGrab
from datetime import datetime


# This is a simple pixel art application using Tkinter. It allows users to create pixel art by clicking on a grid of squares. Each square represents a pixel, and users can choose colors to fill the squares. The application also includes a color palette for selecting colors and a clear button to reset the canvas.
class PixelApp:
    # Initialize the application with the root window
    def __init__(self, root):
        self.root = root
        self.root.title("Pixel Art App")

        # Define the size of each cell in the grid
        cell_length = 50

        # Define the dimensions of the grid (number of cells in width and height)
        grid_width = 20
        grid_height = 10

        # Initialize the color chooser and other variables for tracking the selected color and tools
        self.colour_chooser = colorchooser.Chooser()
        self.chosen_colour = None
        self.is_pencil_selected = False
        self.is_erase_selected = False

        # Create a canvas for drawing the pixel art
        self.drawing_grid = Canvas(self.root)
        self.drawing_grid.grid(row=0, column=0, sticky="nsew")

        # Create a grid of cells (squares) for drawing
        self.cells = []
        for row in range(grid_height):
            for col in range(grid_width):
                cell = Frame(
                    self.drawing_grid,
                    width=cell_length,
                    height=cell_length,
                    bg="white",
                    highlightbackground="black",
                    highlightcolor="black",
                    highlightthickness=1,
                )
                cell.grid(row=row, column=col)
                cell.bind(
                    "<Button-1>", self.tap_cell
                )  # Bind left mouse click to the tap_cell method
                self.cells.append(cell)
        # Create a control frame for color selection and other controls
        control_frame = Frame(self.root, height=cell_length)
        control_frame.grid(row=1, column=0, sticky="news")
        # Add buttons for new project and save project in the control frame
        new_project_btn = Button(
            control_frame, text="New Project", command=self.clear_canvas
        )
        new_project_btn.grid(
            row=0, column=0, columnspan=2, sticky="news", padx=5, pady=5
        )

        save_project_btn = Button(
            control_frame, text="Save Project", command=self.save_canvas
        )
        save_project_btn.grid(
            row=0, column=2, columnspan=2, sticky="news", padx=5, pady=5
        )

        # Add buttons for pen and erase tools in the control frame
        self.pencil_image = PhotoImage(file="pencil.png").subsample(
            2, 3
        )  # Load pencil image
        pencil_btn = Button(
            control_frame,
            text="Pencil",
            image=self.pencil_image,
            command=self.select_pencil,
        )
        pencil_btn.grid(row=0, column=8, columnspan=2, sticky="news", padx=5, pady=5)

        self.eraser_image = PhotoImage(file="eraser.png").subsample(
            2, 3
        )  # Load eraser image
        erase_btn = Button(
            control_frame,
            text="Erase",
            image=self.eraser_image,
            command=self.select_erase,
        )
        erase_btn.grid(row=0, column=10, columnspan=2, sticky="news", padx=5, pady=5)

        # Add a box to display the currently selected color in the control frame
        self.selected_colour_box = Frame(
            control_frame, borderwidth=2, relief="raised", bg="white"
        )
        self.selected_colour_box.grid(row=0, column=15, sticky="nsew", padx=5, pady=8)

        pick_colour_btn = Button(
            control_frame, text="Pick Colour", command=self.pick_colour
        )
        pick_colour_btn.grid(
            row=0, column=17, columnspan=3, sticky="news", padx=5, pady=5
        )

        # Configure the columns in the control frame to have a minimum size equal to the cell length

        cols, rows = control_frame.grid_size()
        for col in range(cols):
            control_frame.grid_columnconfigure(col, minsize=cell_length)
        control_frame.grid_rowconfigure(0, minsize=cell_length)

    def clear_canvas(self):
        # Clear the canvas by resetting the background color of all cells to white
        for cell in self.cells:
            cell.config(bg="white")
            self.selected_colour_box.config(
                bg="white"
            )  # Reset the selected color box to white
        self.chosen_colour = None  # Reset the chosen color
        self.is_pencil_selected = False  # Deselect the pencil tool
        self.is_erase_selected = False  # Deselect the erase tool

    # Save the canvas as an image by capturing the area of the drawing grid and saving it as a PNG file
    def save_canvas(self):
        x = self.root.winfo_rootx() + self.drawing_grid.winfo_x()
        y = self.root.winfo_rooty() + self.drawing_grid.winfo_y()
        width = self.drawing_grid.winfo_width()
        height = self.drawing_grid.winfo_height()

        image_name = (
            datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".png"
        )  # Generate a unique filename based on the current date and time
        _ = ImageGrab.grab().crop((x, y, x + width, y + height)).save(image_name)

    # Methods for selecting tools and picking colors
    def select_pencil(self):
        self.is_pencil_selected = True
        self.is_erase_selected = False

    # When the erase tool is selected, set the chosen color to white and update the color box to reflect this change
    def select_erase(self):
        self.is_erase_selected = True
        self.is_pencil_selected = False
        self.chosen_colour = "white"  # Set the chosen color to white for erasing
        self.selected_colour_box["bg"] = self.chosen_colour  # Update the color box

    # When the user clicks the "Pick Colour" button, open the color chooser dialogue and allow them to select a color. If a color is selected, update the chosen color and the color box to reflect the new selection
    def pick_colour(self):
        colour_info = self.colour_chooser.show()  # Show the color chooser dialogue
        chosen = colour_info[1]  # Get the selected color (hex code)
        if chosen != None:
            self.chosen_colour = chosen  # Store the selected color
            self.selected_colour_box["bg"] = self.chosen_colour  # Update the color box
            self.is_pencil_selected = True
            self.is_erase_selected = False
        # Get the cell that was clicked and change its background color to the chosen color or white if the erase tool is selected

    def tap_cell(self, event):

        widget = event.widget
        index = self.cells.index(widget)
        selected_cell = self.cells[index]
        if self.is_erase_selected:
            selected_cell.config(bg="white")  # Erase the cell by setting it to white
        if self.is_pencil_selected and self.chosen_colour != None:
            selected_cell.config(
                bg=self.chosen_colour
            )  # Set the cell to the chosen color


root = tk.Tk()
PixelApp(root)
root.mainloop()

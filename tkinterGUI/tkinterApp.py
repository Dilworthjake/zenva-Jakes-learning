# A simple To-Do List app built with tkinter. It allows users to add new tasks with descriptions and view the details of existing tasks by selecting them from a list.
from tkinter import *
import tkinter as tk


# Define a class to represent a To-Do item with a name and description
class ToDoItem:

    def __init__(self, name, description):
        self.name = name
        self.description = description


# Define the main application class for the To-Do List app
class ToDoListApp:
    # Initialize the application with the root window and set up the UI components
    def __init__(self, root):

        root.title("To-Do List")

        frame = Frame(root, borderwidth=2, relief="sunken")
        frame.grid(row=1, column=1, sticky="nsew")
        root.columnconfigure(1, weight=1)
        root.rowconfigure(1, weight=1)

        # To Do items section

        # Create a label for the To-Do items list and place it in the grid
        list_label = Label(frame, text="To-Do Items")
        list_label.grid(row=1, column=1, sticky="sw")
        # Initialize a list of To-Do items with some sample tasks
        self.to_do_items = [
            ToDoItem("Gardening", "finish potting the new plants on the terrace"),
            ToDoItem(
                "Sort dinner", "Decide on a meal and get the ingredients and then cook"
            ),
            ToDoItem(
                "Learn tkinter",
                "Finish the tutorial and build a simple app with tkinter",
            ),
        ]
        # Create a StringVar to hold the names of the To-Do items and populate it with the names from the to_do_items list
        self.to_do_names = StringVar(
            value=list(map(lambda x: x.name, self.to_do_items))
        )
        items_list = Listbox(frame, listvariable=self.to_do_names, width=30, height=10)
        items_list.bind(
            "<<ListboxSelect>>", lambda s: self.select_item(items_list.curselection())
        )
        items_list.grid(row=2, column=1, sticky="ew", rowspan=5)

        # Create a StringVar to hold the description of the selected To-Do item and a label to display it
        self.selected_item_description = StringVar()
        selected_description_label = Label(
            frame, textvariable=self.selected_item_description, wraplength=150
        )
        selected_description_label.grid(
            row=7,
            column=1,
            sticky="ew",
        )

        # New Items Section

        # Create a label for the new item section and place it in the grid
        new_item_label = Label(frame, text="Add New Item")
        new_item_label.grid(row=1, column=2, sticky="sw")

        name_label = Label(frame, text="Item name")
        name_label.grid(row=2, column=2, sticky="sw")

        # Create a StringVar to hold the name of the new To-Do item and an entry widget for user input
        self.name = StringVar()
        name_entry = Entry(frame, textvariable=self.name)
        name_entry.grid(row=3, column=2, sticky="new")

        new_item_label = Label(frame, text="Add New Item")
        new_item_label.grid(row=1, column=2, sticky="sw")

        # Create a label for the item description and an entry widget for user input
        description_label = Label(
            frame,
            text="Item description",
        )
        description_label.grid(row=4, column=2, sticky="sw")

        # Create a StringVar to hold the description of the new To-Do item and an entry widget for user input
        self.description = StringVar()
        description_entry = Entry(frame, textvariable=self.description)
        description_entry.grid(row=5, column=2, sticky="new")

        # Create a button to add the new To-Do item and set its command to the add_task method
        save_button = Button(frame, text="Add Task", command=self.add_task)
        save_button.configure(font=("Arial", 14))
        save_button.grid(row=6, column=2, sticky="s")

        # Configure padding for all child widgets in the frame to improve the layout and spacing
        for child in frame.winfo_children():
            child.grid_configure(padx=10, pady=5)

    # Define a method to add a new task to the To-Do list. It creates a new ToDoItem with the name and description from the input fields, adds it to the list of To-Do items, updates the listbox with the new item, and clears the input fields.
    def add_task(self):
        new_item = ToDoItem(self.name.get(), self.description.get())
        self.to_do_items.append(new_item)
        self.to_do_names.set(list(map(lambda x: x.name, self.to_do_items)))
        self.name.set("")
        self.description.set("")

    # Define a method to handle the selection of a To-Do item from the listbox. It retrieves the selected item based on the index, updates the selected_item variable, and sets the description of the selected item to be displayed in the label.
    def select_item(self, index):
        self.selected_item = self.to_do_items[index[0]]
        self.selected_item_description.set(self.selected_item.description)


# Create the main application window and start the Tkinter event loop
root = Tk()
ToDoListApp(root)
root.mainloop()

A lightweight, desktop-based pixel art creator built using Python and Tkinter. This application provides a 20x10 grid interface where users can paint individual grid blocks, pick custom colors, and export their creations as PNG images.

### Features

- Interactive Grid: A 20x10 drawing canvas where each block behaves like a single pixel.

- Custom Color Picker: Integration with the native system color chooser to select any Hex color code.

- Essential Tooling: Quick switching between a Pencil tool for drawing and an Eraser tool to clear specific blocks.

- Export to PNG: Saves your artwork locally with a timestamped filename (e.g., 2026-05-21_16-30-00.png) using an automated screen-cropping capture technique.

- Project Reset: Clear the canvas instantly to start a new design.

### Prerequisites

Before running the application, ensure you have the following installed:

- Python 3.x

- Pillow (PIL Fork): Required for the ImageGrab feature to export images.

You can install Pillow using pip:

- Bash
  1. pip install Pillow
  2. Required Assets
  3. The script expects two small icon images in the same directory as the script:
     - pencil.png (Used for the pencil tool button)

     - eraser.png (Used for the eraser tool button)

### Getting Started

- Clone or download this repository.

- Ensure your pencil.png and eraser.png files are located in the project folder.

- Run the application from your terminal or command prompt:

- Bash
  1. python pixel.py
     (Replace pixel.py with whatever you named your Python file).

### How To Use

- Pick a Color: Click the Pick Colour button to open the palette and select your brush color. The small box next to the button will display your active color.

- Draw: Click the Pencil button (or choose a color to auto-activate it) and left-click on any grid cell.

- Erase: Click the Erase button and left-click any colored grid cell to turn it back to white.

- Save Your Work: Click Save Project to capture the drawing board. The image will save automatically in the project folder.

- Start Fresh: Click New Project to wipe the grid completely clean.

- Note on Saving: The save functionality uses PIL.ImageGrab.grab(), which takes a snapshot based on screen coordinates. Ensure the application window is fully visible on your monitor and not minimized or obstructed when hitting "Save Project".

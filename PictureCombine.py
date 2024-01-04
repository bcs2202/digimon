import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

def select_input_folder():
    input_folder_path = filedialog.askdirectory()
    input_folder_var.set(input_folder_path)

def process_folders():
    input_folder = input_folder_var.get()

    # Get a list of all image files in the input folder
    image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

    if len(image_files) != 9:
        result_label.config(text="Please select exactly 9 images.")
        return

    # Create a canvas to hold the 3x3 arrangement
    canvas = Image.new('RGB', (3 * 431, 3 * 600), 'white')

    # Arrange the images on the canvas
    for i in range(3):
        for j in range(3):
            image_path = os.path.join(input_folder, image_files[i * 3 + j])
            img = Image.open(image_path)
            canvas.paste(img, (j * 431, i * 600))

    # Save the result
    output_folder = filedialog.askdirectory()
    output_path = os.path.join(output_folder, 'output_canvas.jpg')
    canvas.save(output_path)

    result_label.config(text=f"Canvas created and saved: {output_path}")

# Create the main window
app = tk.Tk()
app.title("Image Canvas Creator")

# Variables to store folder path
input_folder_var = tk.StringVar()

# GUI components
input_label = tk.Label(app, text="Select Input Folder:")
input_entry = tk.Entry(app, textvariable=input_folder_var, state='disabled', width=50)
input_button = tk.Button(app, text="Browse", command=select_input_folder)

process_button = tk.Button(app, text="Create Canvas", command=process_folders)
result_label = tk.Label(app, text="")

# Layout
input_label.grid(row=0, column=0, padx=10, pady=5, sticky='e')
input_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')
input_button.grid(row=0, column=2, padx=10, pady=5)

process_button.grid(row=1, column=1, pady=10)
result_label.grid(row=2, column=1)

# Run the main loop
app.mainloop()
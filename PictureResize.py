from tkinter import Tk, Button, Label, filedialog
from PIL import Image, ImageTk
import os

class ImageResizerApp:
    def __init__(self, master):
        self.master = master
        master.title("Image Resizer")

        self.input_folder = ""
        self.output_folder = ""

        self.label_input = Label(master, text="Input Folder:")
        self.label_input.grid(row=0, column=0)

        self.button_input = Button(master, text="Select Input Folder", command=self.select_input_folder)
        self.button_input.grid(row=0, column=1)

        self.label_output = Label(master, text="Output Folder:")
        self.label_output.grid(row=1, column=0)

        self.button_output = Button(master, text="Select Output Folder", command=self.select_output_folder)
        self.button_output.grid(row=1, column=1)

        self.button_resize = Button(master, text="Resize Images", command=self.resize_images)
        self.button_resize.grid(row=2, column=0, columnspan=2)

    def select_input_folder(self):
        self.input_folder = filedialog.askdirectory()
        self.label_input.config(text=f"Input Folder: {self.input_folder}")

    def select_output_folder(self):
        self.output_folder = filedialog.askdirectory()
        self.label_output.config(text=f"Output Folder: {self.output_folder}")

    def resize_images(self):
        if self.input_folder and self.output_folder:
            for filename in os.listdir(self.input_folder):
                input_path = os.path.join(self.input_folder, filename)
                output_path = os.path.join(self.output_folder, filename)

                try:
                    with Image.open(input_path) as img:
                        resized_img = img.resize((431, 600))
                        resized_img.save(output_path)
                except Exception as e:
                    print(f"Error processing {filename}: {e}")
            print("Images resized successfully!")
        else:
            print("Please select input and output folders.")

if name == "__main__":
    root = Tk()
    app = ImageResizerApp(root)
    root.mainloop()
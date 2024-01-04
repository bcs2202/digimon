#pip install pillow
#pip install requests beautifulsoup4

import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import io

class ImageDownloaderGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Downloader")

        # URL Entry
        self.url_label = ttk.Label(master, text="Enter URL:")
        self.url_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        self.url_entry = ttk.Entry(master, width=50)
        self.url_entry.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

        # Image Listbox
        self.image_listbox = tk.Listbox(master, selectmode=tk.MULTIPLE, height=10, width=50)
        self.image_listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky=tk.W)

        # Buttons
        self.show_images_button = ttk.Button(master, text="Show Images", command=self.show_images)
        self.show_images_button.grid(row=2, column=0, pady=10)

        self.select_button = ttk.Button(master, text="Select Images", command=self.select_images_from_subpopup)
        self.select_button.grid(row=2, column=1, pady=10)

        self.download_button = ttk.Button(master, text="Download", command=self.download_images, state=tk.DISABLED)
        self.download_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Image preview variables
        self.image_urls = []
        self.image_previews = []
        self.selected_images = []

    def show_images(self):
        url = self.url_entry.get()

        # Set a user agent in the headers
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

        # Send a GET request to the URL with headers
        response = requests.get(url, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all image tags
            img_tags = soup.find_all('img')

            # Create a new window to show images
            image_window = tk.Toplevel(self.master)
            image_window.title("Available Images")

            # Image Listbox in the new window
            image_listbox = tk.Listbox(image_window, selectmode=tk.MULTIPLE, height=10, width=50)
            image_listbox.pack(padx=10, pady=10)

            # Display image names in the listbox
            for img_tag in img_tags:
                img_src = img_tag.get('src')
                img_url = urljoin(url, img_src)
                img_name = os.path.basename(img_url)
                self.image_urls.append(img_url)
                self.image_previews.append(self.get_image_preview(img_url))
                image_listbox.insert(tk.END, img_name)

            # "Select Images" button
            select_button = ttk.Button(image_window, text="Select Images", command=lambda: self.select_images_from_subpopup(image_listbox))
            select_button.pack(pady=10)

            print("Images loaded successfully in the new window.")

        else:
            print(f"Failed to fetch the page. Status code: {response.status_code}")

    def get_image_preview(self, img_url):
        # Get image content
        img_content = requests.get(img_url).content

        # Convert to PhotoImage
        img = Image.open(io.BytesIO(img_content))
        img.thumbnail((50, 50))  # Adjust the size as needed
        img_preview = ImageTk.PhotoImage(img)

        return img_preview

    def select_images_from_subpopup(self, image_listbox):
        selected_items = image_listbox.curselection()

        # Clear previous selections
        self.selected_images = []

        # Populate selected_images with image previews
        for index in selected_items:
            self.selected_images.append(self.image_previews[index])

        # Close the sub-popup window
        image_listbox.master.destroy()

        # Display selected images in the main GUI
        self.display_selected_images()

        # Enable the "Download" button
        self.download_button["state"] = tk.NORMAL

    def display_selected_images(self):
        # Clear previous image previews
        for widget in self.master.winfo_children():
            if isinstance(widget, tk.Label):
                widget.destroy()

        # Display selected images in the main GUI
        for idx, img_preview in enumerate(self.selected_images):
            img_label = tk.Label(self.master, image=img_preview)
            img_label.grid(row=4, column=idx, padx=5, pady=5)

    def download_images(self):
        if not self.selected_images:
            print("No images selected.")
            return

        url = self.url_entry.get()

        # Set a user agent in the headers
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

        # Send a GET request to the URL with headers
        response = requests.get(url, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all image tags
            img_tags = soup.find_all('img')

            # Download and save selected images to the output folder
            for img_preview in self.selected_images:
                # Find the corresponding index of the selected image in the image previews list
                idx = self.image_previews.index(img_preview)
                img_url = self.image_urls[idx]
                img_content = requests.get(img_url, headers=headers).content
                img_name = os.path.basename(img_url)

                # Create an output folder if it doesn't exist
                output_folder = filedialog.askdirectory(title="Select Output Folder")
                if not output_folder:
                    return

                img_path = os.path.join(output_folder, img_name)

                with open(img_path, 'wb') as img_file:
                    img_file.write(img_content)

                print(f"Image '{img_name}' downloaded and saved to '{output_folder}'.")

        else:
            print(f"Failed to fetch the page. Status code: {response.status_code}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageDownloaderGUI(root)
    root.mainloop()

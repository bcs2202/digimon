import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
import tkinter as tk
from tkinter import ttk

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

        # Download Button
        self.download_button = ttk.Button(master, text="Download Images", command=self.download_images)
        self.download_button.grid(row=2, column=0, columnspan=2, pady=10)

    def download_images(self):
        url = self.url_entry.get()

        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all image tags
            img_tags = soup.find_all('img')

            # Clear existing items in the listbox
            self.image_listbox.delete(0, tk.END)

            # Display image names in the listbox
            for img_tag in img_tags:
                img_src = img_tag.get('src')
                img_url = urljoin(url, img_src)
                img_name = os.path.basename(img_url)
                self.image_listbox.insert(tk.END, img_name)

            print("Images loaded successfully.")
        else:
            print(f"Failed to fetch the page. Status code: {response.status_code}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageDownloaderGUI(root)
    root.mainloop()

##GUI FOR COLOUR, GRAY & BINARY IMAGE DISPLAY
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ImageConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Color, Grayscale & Binary Image Viewer")
        self.image = None

        # Load image button
        self.load_btn = tk.Button(root, text="Load Image", command=self.load_image)
        self.load_btn.pack(pady=5)

        # Option buttons
        self.btn_frame = tk.Frame(root)
        self.btn_frame.pack()

        self.color_btn = tk.Button(self.btn_frame, text="Show Color", command=self.show_color)
        self.color_btn.grid(row=0, column=0, padx=5)

        self.gray_btn = tk.Button(self.btn_frame, text="Show Grayscale", command=self.show_gray)
        self.gray_btn.grid(row=0, column=1, padx=5)

        self.binary_btn = tk.Button(self.btn_frame, text="Show Binary", command=self.show_binary)
        self.binary_btn.grid(row=0, column=2, padx=5)

        # Matplotlib figure
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(pady=10)

    def load_image(self):
        path = filedialog.askopenfilename()
        if path:
            self.image = Image.open(path)
            self.ax.clear()
            self.ax.imshow(self.image)
            self.ax.set_title("Original Color Image")
            self.ax.axis('off')
            self.canvas.draw()

    def show_color(self):
        if self.image:
            self.ax.clear()
            self.ax.imshow(self.image)
            self.ax.set_title("Color Image")
            self.ax.axis('off')
            self.canvas.draw()

    def show_gray(self):
        if self.image:
            gray = self.image.convert("L")
            self.ax.clear()
            self.ax.imshow(gray, cmap='gray')
            self.ax.set_title("Grayscale Image")
            self.ax.axis('off')
            self.canvas.draw()

    def show_binary(self):
        if self.image:
            gray = self.image.convert("L")
            binary = gray.point(lambda x: 255 if x > 150 else 0, mode='1')
            self.ax.clear()
            self.ax.imshow(binary, cmap='gray')
            self.ax.set_title("Binary Image")
            self.ax.axis('off')
            self.canvas.draw()

# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageConverterGUI(root)  

    def on_close():
        root.quit()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()
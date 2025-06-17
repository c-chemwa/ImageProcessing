##BINARY THRESHOLD GUI WITH A THRESHOLD VALUE INPUT SECTION
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ThresholdGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Binary Threshold Viewer")

        self.image = None
        self.gray_image = None

        # Load Button
        self.load_btn = tk.Button(root, text="Load Image", command=self.load_image)
        self.load_btn.pack(pady=5)

        # Threshold Input Section
        input_frame = tk.Frame(root)
        input_frame.pack(pady=5)

        tk.Label(input_frame, text="Threshold (0–255):").pack(side=tk.LEFT, padx=5)
        self.threshold_entry = tk.Entry(input_frame, width=5)
        self.threshold_entry.pack(side=tk.LEFT)
        self.threshold_entry.insert(0, "128")

        self.apply_btn = tk.Button(input_frame, text="Apply Threshold", command=self.apply_threshold)
        self.apply_btn.pack(side=tk.LEFT, padx=5)

        # Matplotlib Canvas
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack()

    def load_image(self):
        path = filedialog.askopenfilename()
        if path:
            image = Image.open(path).convert("L")
            self.image = image
            self.gray_image = np.array(image)
            self.ax.clear()
            self.ax.imshow(self.gray_image, cmap='gray', vmin=0, vmax=255)
            self.ax.set_title("Grayscale Image")
            self.ax.axis('off')
            self.canvas.draw()

    def apply_threshold(self):
        if self.gray_image is None:
            messagebox.showwarning("Warning", "Please load an image first.")
            return

        try:
            threshold = int(self.threshold_entry.get())
            if not (0 <= threshold <= 255):
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Threshold must be an integer between 0 and 255.")
            return

        binary = (self.gray_image > threshold) * 255
        self.ax.clear()
        self.ax.imshow(binary.astype(np.uint8), cmap='gray', vmin=0, vmax=255)
        self.ax.set_title(f"Binary Image (Threshold = {threshold})")
        self.ax.axis('off')
        self.canvas.draw()

# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = ThresholdGUI(root)

    def on_close():
        root.quit()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()
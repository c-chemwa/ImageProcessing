##WITH START AND STOP FUNCTION
import tkinter as tk
from tkinter import filedialog
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ThresholdAnimator:
    def __init__(self, root):
        self.root = root
        self.root.title("Binary Threshold Animation (0–255 Loop)")

        self.image = None
        self.anim = None
        self.running = False
        self.current_frame = 0
        self.thresh_steps = list(range(0, 256, 1))  # 0–255 in steps of 5

        # Load button
        self.load_btn = tk.Button(root, text="Load Image", command=self.load_image)
        self.load_btn.pack(pady=5)

        # Start/Stop buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)

        self.start_btn = tk.Button(btn_frame, text="Start Animation", command=self.start_animation, state='disabled')
        self.start_btn.grid(row=0, column=0, padx=5)

        self.stop_btn = tk.Button(btn_frame, text="Stop Animation", command=self.stop_animation, state='disabled')
        self.stop_btn.grid(row=0, column=1, padx=5)

        # Matplotlib display
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack()

    def load_image(self):
        path = filedialog.askopenfilename()
        if path:
            self.image = Image.open(path).convert("L")
            self.img_array = np.array(self.image)
            self.ax.clear()
            self.ax.imshow(self.image, cmap='gray')
            self.ax.set_title("Grayscale Image")
            self.ax.axis('off')
            self.canvas.draw()
            self.start_btn.config(state='normal')  # Enable start after loading

    def update(self, _):
        thresh = self.thresh_steps[self.current_frame % len(self.thresh_steps)]
        binary = (self.img_array > thresh) * 255
        self.ax.clear()
        self.ax.imshow(binary, cmap='gray', vmin=0, vmax=255)
        self.ax.set_title(f"Threshold = {thresh}")
        self.ax.axis('off')
        self.current_frame += 1
        return [self.ax]

    def start_animation(self):
        if self.image and not self.running:
            self.anim = FuncAnimation(self.fig, self.update, interval=100, blit=False)
            self.canvas.draw()
            self.running = True
            self.start_btn.config(state='disabled')
            self.stop_btn.config(state='normal')

    def stop_animation(self):
        if self.anim:
            self.anim.event_source.stop()
            self.running = False
            self.start_btn.config(state='normal')
            self.stop_btn.config(state='disabled')

# Run GUI
if __name__ == "__main__":
    root = tk.Tk()

    def on_close():
        root.quit()
        root.destroy()

    app = ThresholdAnimator(root)
    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()
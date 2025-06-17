##A PYTHON imnoise() FUNCTION FOR DIFFERENT TYPES OF NOISE 
from PIL import Image
import numpy as np

# Load the image
image = Image.open("assets/mashle.png").convert("RGB")  # or "L" for grayscale


def imnoise(image, noise_type='salt & pepper', amount=0.05, mean=0, var=0.01):
    img = np.array(image).astype(np.float32)
    output = np.copy(img)

    if noise_type == 'salt & pepper':
        num_pixels = img.shape[0] * img.shape[1]
        num_salt = int(amount * num_pixels / 2)
        num_pepper = int(amount * num_pixels / 2)

        # Add salt
        coords = (np.random.randint(0, img.shape[0], num_salt),
                  np.random.randint(0, img.shape[1], num_salt))
        if img.ndim == 2:
            output[coords] = 255
        else:
            output[coords[0], coords[1], :] = 255

        # Add pepper
        coords = (np.random.randint(0, img.shape[0], num_pepper),
                  np.random.randint(0, img.shape[1], num_pepper))
        if img.ndim == 2:
            output[coords] = 0
        else:
            output[coords[0], coords[1], :] = 0

    elif noise_type == 'gaussian':
        sigma = var ** 0.5
        gauss = np.random.normal(mean, sigma, img.shape)
        output = img + gauss * 255
        output = np.clip(output, 0, 255)

    elif noise_type == 'speckle':
        noise = np.random.randn(*img.shape)
        output = img + img * noise * var
        output = np.clip(output, 0, 255)

    else:
        raise ValueError("Unsupported noise type. Use 'salt & pepper', 'gaussian', or 'speckle'.")

    return Image.fromarray(output.astype('uint8'))

##ITS USAGE
#Colour use image and gray scale use gray_scale
# Salt and Pepper
noisy_sp = imnoise(image, noise_type='salt & pepper', amount=0.5)
noisy_sp.show()

# Gaussian Noise
noisy_gaussian = imnoise(image, noise_type='gaussian', mean=0, var=0.5)
noisy_gaussian.show()

# Speckle Noise
noisy_speckle = imnoise(image, noise_type='speckle', var=0.5)
noisy_speckle.show()
          
          
##THE THREE TYPES NOISE ANIMATION WITH GUI 
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys

# Enhanced Noise Function for Color/Grayscale Images
def imnoise(image_array, noise_type='salt & pepper', level=0.05):
    img = np.array(image_array).astype(np.float32)
    output = np.copy(img)

    if len(img.shape) == 2:
        channels = 1
    else:
        channels = img.shape[2]

    def apply_noise_channelwise(noise_fn):
        if channels == 1:
            return noise_fn(img)
        else:
            noisy_img = np.zeros_like(img)
            for c in range(channels):
                noisy_img[..., c] = noise_fn(img[..., c])
            return noisy_img

    if noise_type == 'salt & pepper':
        def sp_noise(channel):
            if level >= 1.0:
                return np.random.choice([0, 255], size=channel.shape)
            output = np.copy(channel)
            num_pixels = channel.shape[0] * channel.shape[1]
            num_salt = int(level * num_pixels / 2)
            num_pepper = int(level * num_pixels / 2)

            coords = (np.random.randint(0, channel.shape[0], num_salt),
                      np.random.randint(0, channel.shape[1], num_salt))
            output[coords] = 255

            coords = (np.random.randint(0, channel.shape[0], num_pepper),
                      np.random.randint(0, channel.shape[1], num_pepper))
            output[coords] = 0
            return output

        output = apply_noise_channelwise(sp_noise)

    elif noise_type == 'gaussian':
        def gaussian_noise_white(channel):
            if level >= 1.0:
                return np.full_like(channel, 255)
            mask = np.random.rand(*channel.shape) < level
            output = np.copy(channel)
            output[mask] = 255
            return output

        output = apply_noise_channelwise(gaussian_noise_white)

    elif noise_type == 'speckle':
        def speckle_noise(channel):
            noise = np.random.randn(*channel.shape)
            output = channel + channel * noise * level
            return np.clip(output, 0, 255)

        output = apply_noise_channelwise(speckle_noise)

    return output.astype(np.uint8)

class NoiseGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Noise Level GUI")
        self.original_image = None
        self.image_array = None
        self.animation = None
        self.anim_running = False
        self.current_level = 0
        self.increment = 1

        self.setup_controls()

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack()

    def setup_controls(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=5)

        tk.Button(control_frame, text="Load Image", command=self.load_image).grid(row=0, column=0, padx=5)

        tk.Label(control_frame, text="Noise Type:").grid(row=0, column=1)
        self.noise_type = tk.StringVar(value="salt & pepper")
        ttk.Combobox(control_frame, textvariable=self.noise_type, state="readonly",
                     values=["salt & pepper", "gaussian", "speckle"], width=15).grid(row=0, column=2, padx=5)

        tk.Label(control_frame, text="Manual %:").grid(row=1, column=0)
        self.manual_entry = tk.Entry(control_frame, width=5)
        self.manual_entry.grid(row=1, column=1)
        tk.Button(control_frame, text="Apply", command=self.apply_manual).grid(row=1, column=2, padx=5)

        tk.Label(control_frame, text="Live Slider:").grid(row=2, column=0)
        self.slider = tk.Scale(control_frame, from_=0, to=100, orient=tk.HORIZONTAL, command=self.apply_slider)
        self.slider.grid(row=2, column=1, columnspan=2, sticky="we")

        anim_frame = tk.Frame(self.root)
        anim_frame.pack(pady=5)

        tk.Button(anim_frame, text="Start Animation", command=self.start_animation).pack(side=tk.LEFT, padx=5)
        tk.Button(anim_frame, text="Stop Animation", command=self.stop_animation).pack(side=tk.LEFT, padx=5)

    def load_image(self):
        path = filedialog.askopenfilename()
        if path:
            img = Image.open(path)
            self.original_image = img
            self.image_array = np.array(img.convert("RGB")) if img.mode != "L" else np.array(img.convert("L"))
            self.current_level = 0
            self.display_image(self.image_array, "Original Image")

    def display_image(self, array, title=""):
        self.ax.clear()
        if len(array.shape) == 2:
            self.ax.imshow(array, cmap='gray', vmin=0, vmax=255)
        else:
            self.ax.imshow(array.astype(np.uint8))
        self.ax.set_title(title)
        self.ax.axis('off')
        self.canvas.draw()

    def apply_manual(self):
        if self.image_array is None:
            messagebox.showwarning("No Image", "Load an image first.")
            return
        try:
            val = float(self.manual_entry.get())
            if not (0 <= val <= 100):
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Enter a value between 0 and 100.")
            return

        level = val / 100.0
        img = imnoise(self.image_array, self.noise_type.get(), level=level)
        self.display_image(img, f"{self.noise_type.get()} Noise ({val}%)")

    def apply_slider(self, val):
        if self.image_array is None:
            return
        level = int(val) / 100.0
        img = imnoise(self.image_array, self.noise_type.get(), level=level)
        self.display_image(img, f"{self.noise_type.get()} Noise ({val}%)")

    def update_animation(self, _):
        if self.image_array is None:
            return
        if self.current_level >= 100:
            self.increment = -1
        elif self.current_level <= 0:
            self.increment = 1

        self.current_level += self.increment
        val = self.current_level
        img = imnoise(self.image_array, self.noise_type.get(), level=val / 100.0)
        self.slider.set(val)
        self.display_image(img, f"{self.noise_type.get()} Noise ({val}%)")

    def start_animation(self):
        if self.image_array is None:
            messagebox.showwarning("No Image", "Load an image first.")
            return
        if not self.anim_running:
            self.anim_running = True
            self.animation = FuncAnimation(self.fig, self.update_animation,
                                           interval=100, cache_frame_data=False)
            self.canvas.draw()

    def stop_animation(self):
        if self.anim_running:
            self.anim_running = False
            if self.animation:
                self.animation.event_source.stop()
                self.animation = None

# Reusable GUI function
def launch_gui():
    root = tk.Tk()
    app = NoiseGUI(root)

    def on_close():
        app.stop_animation()
        root.quit()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()

if __name__ == "__main__":
    launch_gui()


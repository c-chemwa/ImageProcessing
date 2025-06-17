from PIL import Image

# Open the greyscale image
image = Image.open("assets/mashle_gray.png")
# Apply a threshold to convert it to binary (black and white)
threshold = 128
binary_image = image.point(lambda p: 255 if p > threshold else 0)

# Convert to mode '1' (1-bit pixels, black and white)
binary_image = binary_image.convert("1")

# Display the binary image
binary_image.show()

# Save the binary image if needed
binary_image.save("assets/mashle_binary.png")
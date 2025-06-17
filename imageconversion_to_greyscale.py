##TRANSFORM IMAGE TO GRAY SCALE
from PIL import Image

# Open an image file
image = Image.open('assets/mashle.png')

# Display the image
image.show()

# Convert the image to grayscale
gray_image = image.convert('L')

# Display the grayscale image
gray_image.show()

# Save the grayscale image if needed
gray_image.save('assets/mashle_gray.png')
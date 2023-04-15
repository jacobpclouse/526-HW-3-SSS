from PIL import Image

# Open the image file
image = Image.open("grayscale.bmp")

# Set the maximum pixel value to 250
image = image.point(lambda x: min(x, 250))

# Save the modified image
image.save("grayscale_max250.bmp")

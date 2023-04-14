from PIL import Image

# Open the image file
image = Image.open("colored.bmp")

# Set the maximum pixel value to 250
image = image.point(lambda x: min(x, 250))

# Save the modified image
image.save("colored_max250.bmp")

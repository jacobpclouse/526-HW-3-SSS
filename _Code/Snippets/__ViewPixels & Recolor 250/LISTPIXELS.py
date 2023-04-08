from PIL import Image

# Open the image file
image = Image.open("My_output.bmp")

# Convert the image to grayscale
image = image.convert("L")

# Get the pixel data
pixels = list(image.getdata())

# Modify the pixel values
new_pixels = [min(pixel, 250) for pixel in pixels]

# Create a new image object with the modified pixel values
new_image = Image.new(image.mode, image.size)
new_image.putdata(new_pixels)

# Save the new image as a bitmap file
new_image.save("new_example.bmp")
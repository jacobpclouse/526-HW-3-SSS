from PIL import Image

# Open the bitmap image
img = Image.open("grayscale.bmp")

# Get the pixel values
pixels = img.load()

# Get the width and height of the image
width, height = img.size

# Create a new image to store the modified pixels
new_img = Image.new("L", (width, height))

# Get the pixel access object for the new image
new_pixels = new_img.load()

# Iterate through the pixels and modify their values
for y in range(height):
    for x in range(width):
        # Get the grayscale value of the pixel
        grayscale_value = (pixels[x, y][0] + pixels[x, y][1] + pixels[x, y][2]) // 3

        # If the value is greater than 250, set it to 250
        if grayscale_value > 250:
            grayscale_value = 250

        # Set the new pixel value
        new_pixels[x, y] = grayscale_value

# Save the modified image
new_img.save("max250.bmp")

from PIL import Image

# Open the bitmap image
img = Image.open("My_new_example.bmp")

# Get the pixel values
pixels = img.load()

# Get the width and height of the image
width, height = img.size

# Iterate through the pixels and print their values
for y in range(height):
    for x in range(width):
        print(pixels[x, y], end=' ')
    print()

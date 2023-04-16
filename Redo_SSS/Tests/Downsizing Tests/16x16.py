from PIL import Image

# Set the size of the bitmap
WIDTH = HEIGHT = 16 * 4

# Create a new image with the given size and mode
img = Image.new('1', (WIDTH, HEIGHT), color=1)

# Loop through each square and fill it with black or white
for x in range(0, WIDTH, 4):
    for y in range(0, HEIGHT, 4):
        if (x // 4) % 2 == (y // 4) % 2:
            color = 0  # Black
        else:
            color = 1  # White
        # Fill the square with the chosen color
        img.paste(color, (x, y, x+4, y+4))

# Save the image as a bitmap file
img.save('output.bmp')


# from PIL import Image

# # Create a new 16x16 bitmap with a white background
# img = Image.new('1', (16, 16), color=1)

# # Get the pixel access object for the image
# pixels = img.load()

# # Iterate over the pixels and set every other pixel to black
# for x in range(16):
#     for y in range(16):
#         if (x + y) % 2 == 0:
#             pixels[x, y] = 0

# # Save the image to a file
# img.save('alternating.bmp')

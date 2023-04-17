from PIL import Image

# Open the image and convert to the RGB mode
img = Image.open('Only250.bmp').convert('RGB')

# Get the dimensions of the image
width, height = img.size

# Create a new image with half the dimensions
new_width = width // 2
new_height = height // 2
new_img = Image.new('RGB', (new_width, new_height))

# Iterate over the new image pixels and set them to the average of the corresponding 4 pixels in the original image
for x in range(new_width):
    for y in range(new_height):
        # Get the corresponding 4 pixels in the original image
        pixels = [
            img.getpixel((2*x, 2*y)),
            img.getpixel((2*x+1, 2*y)),
            img.getpixel((2*x, 2*y+1)),
            img.getpixel((2*x+1, 2*y+1))
        ]

        r = sum(p[0] for p in pixels) % 251
        g = sum(p[1] for p in pixels) % 251
        b = sum(p[2] for p in pixels) % 251
        # Set the new pixel in the new image
        new_img.putpixel((x, y), (r, g, b))

# Save the new image
new_img.save('Only250_Pillow_image.bmp')

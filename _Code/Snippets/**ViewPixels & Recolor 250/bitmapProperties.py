from PIL import Image

# Open the bitmap image file
image = Image.open('max250.bmp')

# Get the dimensions of the image
width, height = image.size

# Loop through each pixel in the image and print its RGB values
for y in range(height):
    for x in range(width):
        pixel_value = image.getpixel((x, y))
        if isinstance(pixel_value, int):
            print('Pixel at position ({}, {}): Invalid value {}'.format(x, y, pixel_value))
        else:
            r, g, b = pixel_value
            print('Pixel at position ({}, {}): R={}, G={}, B={}'.format(x, y, r, g, b))

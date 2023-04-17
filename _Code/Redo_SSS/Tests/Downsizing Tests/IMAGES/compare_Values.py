from PIL import Image

# open the image file
image = 'My_SSS.bmp'


# open the image file
img = Image.open(image)

# get the image dimensions
width, height = img.size

# create empty arrays to store the pixel values
red_pixels = []
green_pixels = []
blue_pixels = []

# iterate over each pixel in the image
for y in range(height):
    for x in range(width):
        # get the pixel value at (x, y)
        r, g, b = img.getpixel((x, y))
        # append the pixel values to the arrays
        red_pixels.append(r)
        green_pixels.append(g)
        blue_pixels.append(b)

# save the pixel values to a file
with open(f'{image}_pixel_values.txt', 'w') as f:
    f.write("Red pixels: " + str(red_pixels) + "\n")
    f.write("Green pixels: " + str(green_pixels) + "\n")
    f.write("Blue pixels: " + str(blue_pixels) + "\n")

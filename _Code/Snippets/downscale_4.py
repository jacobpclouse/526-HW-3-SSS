from PIL import Image

# Open the image
image = Image.open("1.bmp")

# Get the width and height of the image
width, height = image.size

half_width = width // 2
half_height = height // 2

# Create a new image with half the width and height
new_image = Image.new("RGB", (half_width, half_height))

# Loop through each pixel in the new image
for x in range(new_image.width):
    for y in range(new_image.height):
        # Calculate the indices of the 4 neighboring pixels in the original image
        x1 = x * 2
        y1 = y * 2
        x2 = x1 + 1
        y2 = y1 + 1

        # Get the colors of the neighboring pixels
        pixel1_red,pixel1_green,pixel1_blue = image.getpixel((x1, y1))
        print(f"Red: {pixel1_red}, Green: {pixel1_green}, Blue: {pixel1_blue}")
        pixel2 = image.getpixel((x2, y1))
        pixel3 = image.getpixel((x1, y2))
        pixel4 = image.getpixel((x2, y2))

        # Average the colors of the neighboring pixels and take the mod 251
        r = (pixel1[0] + pixel2[0] + pixel3[0] + pixel4[0]) // 4 % 251
        g = (pixel1[1] + pixel2[1] + pixel3[1] + pixel4[1]) // 4 % 251
        b = (pixel1[2] + pixel2[2] + pixel3[2] + pixel4[2]) // 4 % 251

        # Set the pixel in the new image
        new_image.putpixel((x, y), (r, g, b))

# Save the new image
new_image.save("1_output.bmp")

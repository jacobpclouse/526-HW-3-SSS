from PIL import Image

# Open the input image
input_image = Image.open("1.bmp")

# Get the dimensions of the input image
width, height = input_image.size

# Create a new downscaled image with half the resolution of the input image
downscaled_image = Image.new("RGB", (width // 2, height // 2))

# Iterate over each pixel in the downscaled image
for y in range(downscaled_image.height):
    for x in range(downscaled_image.width):
        # Compute the average of the four pixels in the input image
        pixel_sum = 0
        for dy in range(2):
            for dx in range(2):
                # Get the corresponding pixel in the input image
                px = 2 * x + dx
                py = 2 * y + dy
                pixel = input_image.getpixel((px, py))
                # Add the color values to the sum
                pixel_sum += pixel
        # Compute the average and set the pixel in the downscaled image
        average_pixel = tuple((pixel_sum // 4).to_bytes(3, 'big'))
        downscaled_image.putpixel((x, y), average_pixel)


# Save the downscaled image as a bitmap
downscaled_image.save("2_downscaled_image.bmp")

from PIL import Image

# Load input image
input_image = Image.open("1.bmp")

# Open the input image and get its dimensions
# input_image = Image.open('input_image.bmp')
width, height = input_image.size

# Create a new image with half the dimensions of the input image
downscaled_image = Image.new('RGB', (width // 2, height // 2))

# Iterate over the pixels in the downscaled image
for y in range(height // 2):
    for x in range(width // 2):
        # Get the corresponding four pixels in the input image
        p1 = input_image.getpixel((x * 2, y * 2))
        p2 = input_image.getpixel((x * 2 + 1, y * 2))
        p3 = input_image.getpixel((x * 2, y * 2 + 1))
        p4 = input_image.getpixel((x * 2 + 1, y * 2 + 1))

        print('p1 = ', p1)
        print('p2 = ', p2)
        print('p3 = ', p3)
        print('p4 = ', p4)

        # Calculate the average of the four pixels
        # averaged_pixel = tuple(sum(p) // 4 for p in zip(p1, p2, p3, p4))
        your_tuple = (p1, p2, p3, p4)
        add_values = p1 + p2 + p3 +p4
        print(f"Sum = ",add_values)
        averaged_pixel = add_values // 4

        # Set the pixel value in the downscaled image
        downscaled_image.putpixel((x, y), averaged_pixel)

# Save the downscaled image
downscaled_image.save('downscaled_image.bmp')

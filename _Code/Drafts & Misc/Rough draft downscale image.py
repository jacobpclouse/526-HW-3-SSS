from PIL import Image

# Load the input image
input_image = Image.open('input_image.jpg')

# Get the size of the input image
width, height = input_image.size

# Calculate the size of the output image
new_width = width // 2
new_height = height // 2

# Create a new image with the calculated size
output_image = Image.new('RGB', (new_width, new_height))

# Loop through each pixel of the output image
for x in range(new_width):
    for y in range(new_height):
        
        # Calculate the average of the four pixels in the input image
        r = g = b = 0
        for i in range(2):
            for j in range(2):
                px = input_image.getpixel((2*x+i, 2*y+j))
                r += px[0]
                g += px[1]
                b += px[2]
        r //= 4
        g //= 4
        b //= 4
        
        # Set the pixel value in the output image
        output_image.putpixel((x, y), (r, g, b))

# Save the output image
output_image.save('output_image.jpg')

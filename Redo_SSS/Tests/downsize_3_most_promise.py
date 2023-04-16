from PIL import Image


def downscale_image(orig_image, width, height):
    # Open the image
    img = Image.open(orig_image)

    # Downsize the image by a factor of 2
    # img = img.resize((width//2, img.height//2))

    # Convert the image to grayscale
    img = img.convert('L')
    half_width = width // 2
    print(half_width)
    half_height = height // 2
    print(half_height)

    # Create a new image to hold the downsized image
    new_img = Image.new('L', (half_width, half_height))

    # Loop through each pixel in the downsized image and average the values of the neighboring pixels
    # for y in range(0, half_height, 2):
    for y in range(0, half_height, 2):
        # for x in range(0, half_width, 2):
        for x in range(0, half_width, 2):
            # Get the values of the four neighboring pixels
            pixel1 = img.getpixel((x, y))
            pixel2 = img.getpixel((x+1, y))
            pixel3 = img.getpixel((x, y+1))
            pixel4 = img.getpixel((x+1, y+1))

            # Average the values of the four neighboring pixels and take the result mod 251
            average_value = (pixel1 + pixel2 + pixel3 + pixel4) // 4 % 251

            # Set the value of the corresponding pixel in the new image
            new_img.putpixel((x, y), average_value)

    # Display the new image
    # new_img.show()

    # Save the new image to a file
    new_img.save('output.bmp')


downscale_image('1.bmp',480,640)
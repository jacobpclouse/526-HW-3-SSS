from PIL import Image

# Open the image file
image = Image.open('crop.bmp')

# Get the current dimensions of the image
current_width, current_height = image.size

# Set the dimensions for cropping to the upper left quarter
width = current_width // 2
height = current_height // 2

# Crop the image
cropped_image = image.crop((0, 0, width, height))

# Save the cropped image
cropped_image.save('cropped.bmp')

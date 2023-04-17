import numpy as np
import cv2

# Load the image
img = cv2.imread('path/to/image')

# Get the dimensions of the image
height, width, channels = img.shape

# Downsize the image by two
new_height, new_width = int(height/2), int(width/2)

# Create a new image with the downsampled dimensions
downsampled_img = np.zeros((new_height, new_width, channels), dtype=np.uint8)

# Iterate over the downsampled image and average the neighboring pixels
for i in range(new_height):
    for j in range(new_width):
        # Calculate the indices of the four neighboring pixels
        top_left = (i*2, j*2)
        top_right = (i*2, j*2+1)
        bottom_left = (i*2+1, j*2)
        bottom_right = (i*2+1, j*2+1)
        
        # Average the pixel values of the four neighbors and take modulo 251
        pixel_value = (img[top_left] + img[top_right] + img[bottom_left] + img[bottom_right]) // 4 % 251
        
        # Assign the new pixel value to the downsampled image
        downsampled_img[i, j] = pixel_value

# Save the downsampled image to a file
cv2.imwrite('path/to/output/image', downsampled_img)

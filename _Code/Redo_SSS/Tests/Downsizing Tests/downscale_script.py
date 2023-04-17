import numpy as np
import cv2

# Load the image in grayscale
cvImageOriginal = cv2.imread('Only250.bmp', cv2.IMREAD_GRAYSCALE)

# Get the dimensions of the image
height, width = cvImageOriginal.shape

# Downsize the image by two
new_height, new_width = int(height/2), int(width/2)

# Create a new image with the downsampled dimensions
downsampled_cvImageOriginal = np.zeros((new_height, new_width), dtype=np.uint8)

# Iterate over the downsampled image and average the neighboring pixels
for i in range(new_height):
    for j in range(new_width):
        # Calculate the indices of the four neighboring pixels
        top_left = (i*2, j*2)
        top_right = (i*2, j*2+1)
        bottom_left = (i*2+1, j*2)
        bottom_right = (i*2+1, j*2+1)
        
        # Average the pixel values of the four neighbors and take modulo 251
        pixel_value = (cvImageOriginal[top_left] + cvImageOriginal[top_right] + cvImageOriginal[bottom_left] + cvImageOriginal[bottom_right]) // 4 % 251
        
        # Assign the new pixel value to the downsampled image
        downsampled_cvImageOriginal[i, j] = pixel_value

# Save the downsampled image to a file
cv2.imwrite('Only250_openCV_downscaled.bmp', downsampled_cvImageOriginal)

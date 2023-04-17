import numpy as np
import cv2

# needs to be black and white before using
# SOURCE: Image Resizing with OpenCV: https://learnopencv.com/image-resizing-with-opencv/
# Load the image
cvImageOriginal = cv2.imread('blackbuck.bmp') # orig
# cvImageOriginal = cv2.imread('blackbuck.bmp', cv2.IMREAD_GRAYSCALE)


# Get the dimensions of the image
height, width, channels = cvImageOriginal.shape

# Downsize the image by two
new_height, new_width = int(height/2), int(width/2)

# Create a new image with the downsampled dimensions
downsampledcvImageOriginal = np.zeros((new_height, new_width, channels), dtype=np.uint8)

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
        downsampledcvImageOriginal[i, j] = pixel_value

# Save the downsampled image to a file
cv2.imwrite('blackbuck_openCV_downscaled.bmp', downsampledcvImageOriginal)

import random
from PIL import Image
import numpy as np
import cv2


# --- Downscale Image Method 2 ---
# SOURCE: Image Resizing with OpenCV: https://learnopencv.com/image-resizing-with-opencv/
def downscale_image(inputImage, shareNo):
    print(f"Downscaling {shareNo} With OpenCV...")
    # print(f"Need to make the image: {(width_in//2)} by {(height_in//2)}")
    cvImageOriginal = cv2.imread(inputImage) # needs to be black and white before using, but we have already taken care of that
    height, width, channels = cvImageOriginal.shape
    half_height, half_width = int(height/2), int(width/2) # get the new dimensions for output image
    downsampledcvImageOriginal = np.zeros((half_height, half_width, channels), dtype=np.uint8) # create new image, using new dimensions
    # new_array_pixel_values = []
    # average x4 pixels by going through them
    for i in range(half_height):
        for j in range(half_width):
            # Calculate the indices of the four neighboring pixels
            top_left = (i*2, j*2)
            top_right = (i*2, j*2+1)
            bottom_left = (i*2+1, j*2)
            bottom_right = (i*2+1, j*2+1)
            
            # Average the pixel values of the four neighbors and take modulo 251
            pixel_value = (cvImageOriginal[top_left] + cvImageOriginal[top_right] + cvImageOriginal[bottom_left] + cvImageOriginal[bottom_right]) // 4 % 251
            
            # Assign the new pixel value to the downsampled image
            downsampledcvImageOriginal[i, j] = pixel_value

            # new_array_pixel_values.append(pixel_value)

    # Save the downsampled image to a file and return the values
    cv2.imwrite("controlImage.bmp", downsampledcvImageOriginal)
    return half_width, half_height, downsampledcvImageOriginal #use the last value to get the MAE



new_width, new_height, new_array_boi = downscale_image("3.bmp", "Test", "Test2","Control Image 2")
from PIL import Image
import numpy as np

# Load the two images
img_o = Image.open('colored.bmp')
img_s = Image.open('grayscale_max250.bmp')

# Convert the images to numpy arrays
arr_o = np.array(img_o)
arr_s = np.array(img_s)

# Calculate the absolute difference between the two arrays
abs_diff = np.abs(arr_o - arr_s)

# Calculate the sum of the absolute differences over all pixels
sum_abs_diff = np.sum(abs_diff)

# Calculate the total number of pixels
num_pixels = arr_o.shape[0] * arr_o.shape[1]

# Calculate the mean average error
mae = sum_abs_diff / num_pixels

# Print the result
print("The mean average error between the two images is: ", mae)

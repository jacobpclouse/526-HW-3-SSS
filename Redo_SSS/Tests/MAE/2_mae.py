import numpy as np
from PIL import Image

def calculate_mae(img1_path, img2_path):
    # Load the images and convert them to numpy arrays
    img1 = np.array(Image.open(img1_path).convert('L')) # convert to grayscale
    img2 = np.array(Image.open(img2_path).convert('L'))

    # Calculate the absolute difference between the pixel values of two images
    diff = np.abs(img1 - img2)

    # Calculate the sum of absolute differences and divide by the total number of pixels
    mae = np.sum(diff) / (img1.shape[0] * img1.shape[1])

    return mae

# Example usage
img1_path = 'colored.bmp'
img2_path = 'grayscale_max250.bmp'

mae = calculate_mae(img1_path, img2_path)
print("Mean Average Error: ", mae)

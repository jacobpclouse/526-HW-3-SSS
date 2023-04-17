from PIL import Image
import numpy as np
from scipy.interpolate import lagrange as lag

# Set variables
n = 5 # Number of shares to generate
r = 3 # Number of shares needed to reconstruct
path = "test2.png" # Path to input image

# Function to read an image and convert it to grayscale
def read_image(path):
    img = Image.open(path).convert('L') 
    img_array = np.asarray(img) # Convert image to a numpy array
    return img_array.flatten(), img_array.shape # Flatten the array and return it with its shape

# Function to generate shares using a polynomial function
def polynomial(img, n, r):
    num_pixels = img.shape[0] # Get the total number of pixels in the image
    coef = np.random.randint(low = 0, high = 251, size = (num_pixels, r - 1)) # Generate an array of random coefficients for the polynomial function
    gen_imgs = []
    for i in range(1, n + 1):
        base = np.array([i ** j for j in range(1, r)]) # Generate the base for the polynomial function
        base = np.matmul(coef, base) # Multiply the coefficients with the base to generate the shares
        img_ = img + base # Add the shares to the original image
        img_ = img_ % 251 # Take the modulo to ensure values are within the range [0, 250]
        gen_imgs.append(img_)
    return np.array(gen_imgs)

# Function to decode the shares and reconstruct the original image
def decode(imgs, index, r, n):
    assert imgs.shape[0] >= r # Check that there are at least r shares
    x = np.array(index) # Convert the index list to a numpy array
    dim = imgs.shape[1] # Get the dimension of the image
    img = []
    for i in range(dim):
        if (i + 1) % 10000 == 0:
            print("Decoding {}th pixel".format(i + 1))
        y = imgs[:, i] # Get the shares for the current pixel
        poly = lag(x, y) # Use Lagrange interpolation to reconstruct the polynomial function
        pixel = poly(0) % 251 # Evaluate the function at x=0 to get the pixel value
        img.append(pixel)
    return np.array(img)

# Main function
if __name__ == "__main__":
    img_flattened, shape = read_image(path) # Read the input image
    gen_imgs = polynomial(img_flattened, n, r) # Generate the shares
    to_save = gen_imgs.reshape(n, *shape) # Reshape the shares for saving
    for i, img in enumerate(to_save):
        Image.fromarray(img.astype(np.uint8)).save("test2_{}.jpeg".format(i + 1)) # Save each share as a separate image
    origin_img = decode(gen_imgs[0:r, :], list(range(1, r + 1)), r, n) # Decode the shares to reconstruct the original image
    origin_img = origin_img.reshape(*shape)
    Image.fromarray(origin_img.astype(np.uint8)).save("test2_origin.jpeg") # Save the reconstructed image

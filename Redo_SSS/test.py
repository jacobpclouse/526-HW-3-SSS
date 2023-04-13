from PIL import Image
import numpy as np
#from scipy.interpolate import lagrange as lag

def read_image(path):
    img = Image.open(path).convert('L') # this converts to grayscale
    # img.show()
    img_array = np.asarray(img)
    print(img_array.shape) # this is the dimensions that we are getting 
    
    return img_array.flatten(), img_array.shape
    # The flatten() method is used to convert a multidimensional array into a one-dimensional array or a vector.



# Function to split an image into shares using Shamir's Secret Sharing algorithm
def split_image_shamir(image_path):
    # Load the image
    with open(image_path, "rb") as f:
        # header = f.read(54) # BMP header is 54 bytes long
        img_bytes = f.read()
    img_data = np.frombuffer(img_bytes, dtype=np.uint8)
    return img_data


array1, arrayShape = read_image('1.bmp')
array2 = split_image_shamir('1.bmp')
print(array1)
print(array2)


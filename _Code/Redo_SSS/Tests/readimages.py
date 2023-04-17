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


'''
The two functions read_image() and split_image_shamir() are using different methods to read and process the image data, which can lead to different results.

The read_image() function is using the Python Imaging Library (PIL) to open and read the image file. It then converts the image to grayscale and converts it to a NumPy array using np.asarray(). Finally, it calls flatten() to convert the two-dimensional NumPy array into a one-dimensional array.

On the other hand, the split_image_shamir() function is using numpy.frombuffer() to read the image data directly from the file as a byte string. It then converts the byte string into a NumPy array using np.frombuffer() without any additional processing.

The difference in the output of these two functions is likely due to the way the image data is being read and processed. The read_image() function is converting the image to grayscale and flattening it, while the split_image_shamir() function is only reading the raw image data without any additional processing.


'''

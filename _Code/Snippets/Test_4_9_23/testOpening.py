import numpy as np
import random
from PIL import Image


# Function to split an image into shares using Shamir's Secret Sharing algorithm
def split_image_shamir(image_path):
    # Load the image from 251
    with open(image_path, "rb") as f:
        header = f.read(54) # BMP header is 54 bytes long
        img_bytes = f.read()
    img_data_251 = np.frombuffer(img_bytes, dtype=np.uint8)
    

    # load image from working shamir
    with open(image_path, "rb") as f:
        header_data = f.read(54) # read the bitmap header information
        image_data = f.read()
    binary_data = "".join(format(byte, "08b") for byte in image_data)

'''
No, the code will not produce the same output because the two code blocks are doing different things.

The first block of code is loading an image as a numpy array using np.frombuffer() after reading the BMP header from the file. The output will be a numpy array representing the image in binary format.

The second block of code is loading an image as binary data, then converting each byte of the image data to an 8-bit binary string representation using format(byte, "08b") and concatenating them together using join(). The output will be a binary string representing the image data in a concatenated format.

Therefore, the first block of code will produce a numpy array representing the image, while the second block of code will produce a concatenated binary string representing the image data.
'''

    # # # # save string to file
    # text_file = open(f"img_data_251.txt", "w")
    # n = text_file.write(img_data_251)
    # text_file.close()



    # # # # save string to file
    # text_file = open(f"image_data_working_shamir.txt", "w")
    # n = text_file.write(binary_data)
    # text_file.close()



split_image_shamir('1.bmp')
import numpy as np
import random
from PIL import Image


def split_image(image_path):
    # load image from working shamir
    with open(image_path, "rb") as f:
        header_data = f.read(54) # read the bitmap header information
        image_data = f.read()
    binary_data = "".join(format(byte, "08b") for byte in image_data)


    
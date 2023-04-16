import random
from PIL import Image
import numpy as np
import cv2

# --- Function to read in an image and adjust to only 250 max values --- 
# SOURCE: http://paulbourke.net/dataformats/bitmaps/
def max_250(origImage,newOutputName):
    # Open the image file
    image = Image.open(origImage)

    # Convert the image to grayscale
    image = image.convert("L")

    # Get the pixel data
    pixels = list(image.getdata())

    # Modify the pixel values
    new_pixels = [min(pixel, 250) for pixel in pixels]

    # Create a new image object with the modified pixel values
    new_image = Image.new(image.mode, image.size)
    new_image.putdata(new_pixels)

    # Save the new image as a bitmap file
    new_image.save(newOutputName)

inputImage = 'test.bmp'
new250Image = 'Only250.bmp'
max_250(inputImage,new250Image)
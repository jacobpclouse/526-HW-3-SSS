from PIL import Image

# Open the image file
img = Image.open("path/to/image.jpg")

# Read the first 54 bytes of the image
with open("path/to/image.jpg", "rb") as f:
    header = f.read(54)


'''
In the above code, we first import the Image module from the PIL library. Then, we open the image file using the Image.open() function and store the result in the img variable.

Next, we use the open() function again, but this time we open the file in binary mode ("rb") and read the first 54 bytes into the header variable.

For bitmap, just use:

with open("path/to/image.bmp", "rb") as f:
    header = f.read(54)

'''
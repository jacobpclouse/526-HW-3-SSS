#https://stackoverflow.com/questions/46385999/transform-an-image-to-a-bitmap

from PIL import Image
import numpy as np

# img = Image.open('road.jpg')
Choose_image = input("Input name of image (with Extension): ")
Choose_output_name = input("Choose Output name (no Extension): ")
img = Image.open(Choose_image)
ary = np.array(img)

# Split the three channels
r,g,b = np.split(ary,3,axis=2)
r=r.reshape(-1)
g=r.reshape(-1)
b=r.reshape(-1)

# Standard RGB to grayscale 
bitmap = list(map(lambda x: 0.299*x[0]+0.587*x[1]+0.114*x[2], 
zip(r,g,b)))
bitmap = np.array(bitmap).reshape([ary.shape[0], ary.shape[1]])
bitmap = np.dot((bitmap > 128).astype(float),255)
im = Image.fromarray(bitmap.astype(np.uint8))
# im.save('road.bmp')
im.save(f'{Choose_output_name}.bmp')
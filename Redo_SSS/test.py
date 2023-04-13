from PIL import Image
import numpy as np
#from scipy.interpolate import lagrange as lag

def read_image(path):
    img = Image.open(path).convert('L') # this converts to grayscale
    # img.show()
    img_array = np.asarray(img)
    # print(img_array.shape) # this is the dimensions that we are getting 
    flatBoi = img_array.flatten()
    # print(flatBoi)
    # print(img_array.flatten())
    num_pix = (img_array.flatten()).shape[0] # gives us the number of pixels in the array
    return flatBoi, img_array.shape, num_pix
    # The flatten() method is used to convert a multidimensional array into a one-dimensional array or a vector.

def polynomial(img, numberOfTotalShares, minNumOfSharesToReconstruct):
    num_pixels = img.shape[0] # this gets the total number of pixels in the image
    coef = np.random.randint(low = 0, high = 251, size = (num_pixels, minNumOfSharesToReconstruct - 1))
    print(coef) # all the coefficients for all the pixel values, which we will use to encrypt this values
    # print(coef.shape)


# n = numberOfTotalShares
# r = minNumOfSharesToReconstruct
# n = 5
# r = 3
path = "1.bmp"
img_flattened, shape, numberPixels= read_image(path)
gen_imgs = polynomial(img_flattened, n = n, r = r)


'''

'''

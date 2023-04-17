# This Python Program was written on Linux Mint and Windows 10 using VScode, your milage may vary on OS and configuration.

'''
This program is a visual implimentation of:
  __                              __                                 __                            
 /    /              /           /                        /         /    /              /          
(___ (___  ___  _ _    ___      (___  ___  ___  ___  ___ (___      (___ (___  ___  ___    ___  ___ 
    )|   )|   )| | )| |   )         )|___)|    |   )|___)|             )|   )|   )|   )| |   )|   )
 __/ |  / |__/||  / | |          __/ |__  |__  |    |__  |__        __/ |  / |__/||    | |  / |__/ 
                                                                                              __/  
Total shares = 5
Required shares to retrieve the original image = 2
'''

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Importing Libraries / Modules 
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
import random
from PIL import Image

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Functions
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

'''combine with encryption function, do image shares inside this'''
# --- Function to read in an image, adjust to only 250 max values, and then output image data in an array --- 
# SOURCE: http://paulbourke.net/dataformats/bitmaps/
def set_image_max_pixel_value(path, max_value=None, ):
    img = Image.open(path).convert('L')
    img_array = []
    width, height = img.size
    for y in range(height):
        for x in range(width):
            pixel = img.getpixel((x, y))
            if max_value is not None:
                pixel = min(pixel, max_value)
            img_array.append(pixel)
    return img_array, (width, height)


def polynomial(img, n, r):
    num_pixels = len(img)
    coef = [[random.randint(0, 250) for _ in range(r-1)] for _ in range(num_pixels)]
    gen_imgs = []
    for i in range(1, n + 1):
        base = [i ** j for j in range(1, r)]
        img_ = []
        for p in range(num_pixels):
            base_sum = sum([coef[p][j] * base[j] for j in range(r-1)])
            img_.append((img[p] + base_sum) % 251)
        gen_imgs.append(img_)
    return gen_imgs


def lagrange(x, y, num_points, x_test):
    l = [0] * num_points
    for k in range(num_points):
        l[k] = 1
        for k_ in range(num_points):
            if k != k_:
                l[k] = l[k] * (x_test - x[k_]) / (x[k] - x[k_])
            else:
                pass
    L = 0
    for i in range(num_points):
        L += y[i] * l[i]
    return L


def decode(imgs, index, r, n):
    assert len(imgs) >= r
    x = index
    dim = len(imgs[0])
    img = []
    for i in range(dim):
        y = [imgs[j][i] for j in range(r)]
        pixel = lagrange(x, y, r, 0) % 251
        img.append(pixel)
    return img


# REMEMBER TO REMOVE THIS!!!!
'''
def set_image_max_pixel_value(path, max_value=None):
    img = Image.open(path).convert('L')
    # img.show()
    img_array = []
    width, height = img.size
    for y in range(height):
        for x in range(width):
            pixel = img.getpixel((x, y))
            if max_value is not None:
                pixel = min(pixel, max_value)
            img_array.append(pixel)
    return img_array, (width, height)


def polynomial(img, n, r):
    num_pixels = len(img)
    coef = [[random.randint(0, 250) for _ in range(r-1)] for _ in range(num_pixels)]
    gen_imgs = []
    for i in range(1, n + 1):
        base = [i ** j for j in range(1, r)]
        img_ = []
        for p in range(num_pixels):
            base_sum = sum([coef[p][j] * base[j] for j in range(r-1)])
            img_.append((img[p] + base_sum) % 251)
        gen_imgs.append(img_)
    return gen_imgs

'''



# --- Function to print out my Logo ---
def myLogo():
    print("Created and Tested by: ")
    print("   __                  _         ___ _                       ")
    print("   \ \  __ _  ___ ___ | |__     / __\ | ___  _   _ ___  ___  ")
    print("    \ \/ _` |/ __/ _ \| '_ \   / /  | |/ _ \| | | / __|/ _ \ ")
    print(" /\_/ / (_| | (_| (_) | |_) | / /___| | (_) | |_| \__ \  __/ ")
    print(" \___/ \__,_|\___\___/|_.__/  \____/|_|\___/ \__,_|___/\___| ")
    print("Dedicated to Peter Zlomek and Harely Alderson III")

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Variables
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
totalNumberOfShares = 5
requiredSharesToRetrieve = 2

inputImage = '1.bmp'
new250Image = 'Only250.bmp'


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# MAIN 
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# myLogo()

if __name__ == "__main__":
    path = "1.bmp"
    n = 5
    r = 3
    # img_flattened, shape = read_image(path)
    img_flattened, shape = set_image_max_pixel_value(path,max_value=250)
    gen_imgs = polynomial(img_flattened, n=n, r=r)
    to_save = [Image.new("L", shape) for _ in range(n)]
    for i, img in enumerate(gen_imgs):
        to_save[i].putdata(img)
        to_save[i].save("test2_{}.jpeg".format(i + 1))
    origin_img = decode(gen_imgs[0:r], list(range(1, r + 1)), r=r, n=n)

img = Image.new("L", shape, color=0)
img.putdata(list(origin_img))
img.save("test2_origin.jpeg")



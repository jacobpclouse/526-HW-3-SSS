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


# --- Function to read in an image, adjust to only 250 max values, and generate shares --- 
# SOURCE: http://paulbourke.net/dataformats/bitmaps/
def split_image_shamir(path, n, r, max_value=None):
    # make sure that we don't have pixel values greater than 250
    img = Image.open(path).convert('L')
    img_array = []
    width, height = img.size
    for y in range(height):
        for x in range(width):
            pixel = img.getpixel((x, y))
            if max_value is not None:
                pixel = min(pixel, max_value)
            img_array.append(pixel)

    # grab coefficents
    # SOURCE: https://www.geeksforgeeks.org/implementing-shamirs-secret-sharing-scheme-in-python/
    coef = [[random.randint(0, 250) for _ in range(r-1)] for _ in range(len(img_array))]
    gen_imgs = []
    for i in range(1, n + 1):
        base = [i ** j for j in range(1, r)]
        img_ = []
        for p in range(len(img_array)):
            base_sum = sum([coef[p][j] * base[j] for j in range(r-1)])
            img_.append((img_array [p] + base_sum) % 251)
        gen_imgs.append(img_)
    # return gen_imgs,(width, height)
    # can we put the image generation inside this function?

    to_save = [Image.new("L", (width, height)) for _ in range(n)]
    for i, imgOut in enumerate(gen_imgs):
        to_save[i].putdata(imgOut)
        to_save[i].save("share{}.bmp".format(i + 1))

    print("Encrypted Shares Generated!")
    return gen_imgs,(width, height)



# --- Function to reconstruct the secret using Lagrange function ---
# SOURCE: https://github.com/cfgnunes/numerical-methods-python/blob/main/interpolation.py
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

    # print("Lagrange Function Executed!")
    return L




# --- Function to reconstruct the original image using the shares ---
# SOURCE: https://www.geeksforgeeks.org/implementing-shamirs-secret-sharing-scheme-in-python/
def decode(imgs, index, r, n):
    assert len(imgs) >= r
    x = index
    dim = len(imgs[0])
    img = []
    for i in range(dim):
        y = [imgs[j][i] for j in range(r)]
        pixel = lagrange(x, y, r, 0) % 251
        img.append(pixel)
        
    print("Decrypted Image Restored!")
    return img



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
# MAIN 
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# myLogo()

# LET THE USER SET THESE
path = "1.bmp"
n = 5
r = 3


'''ENCRYPTION'''
gen_imgs,shape = split_image_shamir(path,n=n, r=r,max_value=250) # change r and n names 

# idea have a varible to ask if they want to downsize/use homomorphism ************
#   We can then have it break off inside the function if so to either function **********

# to_save = [Image.new("L", shape) for _ in range(n)]
# for i, img in enumerate(gen_imgs):
#     to_save[i].putdata(img)
#     to_save[i].save("share{}.bmp".format(i + 1))



''' DECRYPTION'''    
origin_img = decode(gen_imgs[0:r], list(range(1, r + 1)), r=r, n=n)


# save output
img = Image.new("L", shape, color=0)
img.putdata(list(origin_img))
img.save("reconstructed.bmp")



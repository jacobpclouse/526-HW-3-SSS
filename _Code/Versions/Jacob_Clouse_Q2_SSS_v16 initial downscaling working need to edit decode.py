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
def split_image_shamir(path,downscaleBool,n,r,max_value=None):
    # make sure that we don't have pixel values greater than 250, SOURCE: https://thepythonguru.com/python-builtin-functions/max/
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


    ''' NON DOWNSCALING'''
    # Reconstruction data
    array_bits = gen_imgs[0:r]
    decode_list = list(range(1, r + 1))
    
    share_names = []
    # Create Share value images 
    to_save = [Image.new("L", (width, height)) for _ in range(n)]
    for i, imgOut in enumerate(gen_imgs):
        to_save[i].putdata(imgOut)
        name_of_share = "share{}.bmp".format(i + 1)
        to_save[i].save(name_of_share)
        share_names.append(name_of_share)
    # for labels in share_names:
    #     print(labels)


    if downscaleBool == True:
        '''DOWN SCALING'''
        # array_bits = gen_imgs[0:r]
        # decode_list = list(range(1, r + 1))

        # for i, imgOut in enumerate(gen_imgs):
        for labels in share_names:
            new_width, new_height = downscale_image(labels, width, height)
            
        width = new_width
        height = new_height





        # scaled_gen_imgs = []
        # for i in range(n):
        #     scaled_img, half_width, half_height= downscale_image(gen_imgs[i], width, height)
        #     scaled_gen_imgs.append(scaled_img)

        # # Reconstruction data - downscaled
        # array_bits = scaled_gen_imgs[0:r]
        # decode_list = list(range(1, r + 1))

        # # Create Share value images - downscale
        # to_save = [Image.new("L", (half_width, half_height)) for _ in range(n)]
        # for i, imgOut in enumerate(scaled_gen_imgs):
        #     to_save[i].putdata(imgOut)
        #     to_save[i].save("share{}.bmp".format(i + 1))

        print("Encrypted Shares Generated!")

    return gen_imgs,(width, height),array_bits,decode_list


# --- Downscale Image Method ---
def downscale_image(orig_image, width, height):
    # Open the image and convert to the RGB mode, halve dimensions
    img = Image.open(orig_image).convert('RGB')
    half_width = width // 2
    half_height = height // 2
    new_img = Image.new('RGB', (half_width, half_height))

    # Iterate over the new image pixels
    for x in range(half_width):
        for y in range(half_height):
            # Get the corresponding 4 pixels in the original image
            pixels = [
                img.getpixel((2*x, 2*y)),
                img.getpixel((2*x+1, 2*y)),
                img.getpixel((2*x, 2*y+1)),
                img.getpixel((2*x+1, 2*y+1))
            ]
            # mod 251 - so no errors
            r = sum(p[0] for p in pixels) % 251
            g = sum(p[1] for p in pixels) % 251
            b = sum(p[2] for p in pixels) % 251
            # Set the new pixel in the new image
            new_img.putpixel((x, y), (r, g, b))

    # Save the new image share over original
    # new_img.save('output_image.bmp')
    new_img.save(orig_image)
    return half_width, half_height
    # return down_image, down_width, down_height


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

    # print("Lagrange Function Executed!") # TOO MANY PRINT OUTS
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

# LET THE USER SET THESE with input
path = "1.bmp"
n = 5
r = 3
wantDownscale = True

'''ENCRYPTION'''
gen_imgs,shape,arr_bit,list_bit = split_image_shamir(path,wantDownscale,n=n,r=r,max_value=250) # change r and n names 

# idea have a varible to ask if they want to downsize/use homomorphism ************
#   We can then have it break off inside the function if so to either function **********




''' DECRYPTION'''    
origin_img = decode(arr_bit, list_bit, r=r, n=n)


# save output
img = Image.new("L", shape, color=0)
img.putdata(list(origin_img))
img.save("reconstructed.bmp")



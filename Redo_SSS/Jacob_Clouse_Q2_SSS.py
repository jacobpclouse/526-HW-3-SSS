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
import numpy as np
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Functions
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-


# --- Function to read in an image, adjust to only 250 max values, and generate shares ---
# SOURCE: http://paulbourke.net/dataformats/bitmaps/
def split_image_shamir(inputImage,downscaleBool,n,r,max_value=None):
    # make sure that we don't have pixel values greater than 250, SOURCE: https://thepythonguru.com/python-builtin-functions/max/
    imgOpened = Image.open(inputImage).convert('L')
    openedImageArray = []
    width, height = imgOpened.size
    for y in range(height):
        for x in range(width):
            pixel = imgOpened.getpixel((x, y))
            if max_value is not None:
                pixel = min(pixel, max_value)
            openedImageArray.append(pixel)

    # grab coefficents
    # SOURCE: https://www.geeksforgeeks.org/implementing-shamirs-secret-sharing-scheme-in-python/
    coef = [[random.randint(0, 250) for _ in range(r-1)] for _ in range(len(openedImageArray))]
    gen_imgs = []
    for i in range(1, n + 1):
        base = [i ** j for j in range(1, r)]
        img_ = []
        for p in range(len(openedImageArray)):
            base_sum = sum([coef[p][j] * base[j] for j in range(r-1)])
            img_.append((openedImageArray [p] + base_sum) % 251)
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

    new_array_boi = []
    # checks to see if downscaling is active
    if downscaleBool == True:
        '''DOWN SCALING'''
        print("Downscaling Activated!")
        for labels in share_names:
            new_width, new_height, new_array_boi = downscale_image(labels, width, height)

        width = new_width
        height = new_height
        # array_bits = new_array_boi

    else:
        print("No Downscaling Requested!")


        print("Encrypted Shares Generated!")

    return gen_imgs,(width, height),array_bits,decode_list,new_array_boi


# --- Downscale Image Method ---
def downscale_image(orig_image, width, height):
    # Open the image and convert to the RGB mode, halve dimensions
    img = Image.open(orig_image).convert('RGB')
    half_width = width // 2
    half_height = height // 2
    new_img = Image.new('RGB', (half_width, half_height))
    new_array_bits = []
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

    # redo the size
            new_array_bits.append(pixels[0:r])

    # Save the new image share over original
    new_img.save(orig_image)
    return half_width, half_height, new_array_bits
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


# --- Function to decode downsized pics ---
def decode_downsize(imgs, index, r, n):
    # you can also just re open up the share by passing in the name and get the dimensions that way
    assert len(imgs) >= r
    x = index
    # print(x)
    # print(len(imgs[0]))
    dim = len(imgs[0]) // 4
    img = []
    for i in range(dim):
        y = [imgs[j][i] for j in range(r)]
        # print(y)
        pixel = lagrange(x, y, r, 0) % 251
        img.append(pixel)

    print("Decrypted Image Restored!")
    return img

# --- Function to calculate the MAE ---
def calculate_mae(img1_path, img2_path):
    # Load the images and convert them to numpy arrays
    img1 = np.array(Image.open(img1_path).convert('L')) # convert to grayscale
    img2 = np.array(Image.open(img2_path).convert('L'))

    # Calculate the absolute difference between the pixel values of two images
    diff = np.abs(img1 - img2)

    # Calculate the sum of absolute differences and divide by the total number of pixels
    mae = np.sum(diff) / (img1.shape[0] * img1.shape[1])
    print(f"Mean Average Error between {img1_path} & {img2_path}: {mae}")

    return mae

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
useThisImage = "1.bmp"
totalNumberOfShares = 5
minNumberOfShares = 3
wantDownscale = True
reconstructName = "reconstructed.bmp"

'''ENCRYPTION'''
gen_imgs,shape,arr_bit,list_bit,downscaled_array = split_image_shamir(useThisImage,wantDownscale,totalNumberOfShares,minNumberOfShares,max_value=250) # change r and n names


''' DECRYPTION'''
# NEED TO DO SEPERATE FUNCTION IF DOWNSCALING WAS REQUESTED
'''NO DOWNSCALE'''
if wantDownscale == False:
    origin_img = decode(arr_bit, list_bit, minNumberOfShares, totalNumberOfShares)
    # save output
    img = Image.new("L", shape, color=0)
    img.putdata(list(origin_img))
    img.save(reconstructName)
else:
    '''DOWNSCALE'''
    # only 1/4 of length
    origin_img = decode_downsize(arr_bit, list_bit, minNumberOfShares, totalNumberOfShares)

    # pass in width and height
    # save output (width and height half)
    img = Image.new("L", shape, color=0)
    img.putdata(list(origin_img))
    img.save(reconstructName)

    # MAE
    for i in range(totalNumberOfShares):
        shareName = f'share{i+1}.bmp'
        ourMae = calculate_mae(reconstructName,shareName)

'''
    # JUST REOPEN THE IMAGE AGAIN AND GET ORIGIN VALS
    I_s = np.array(Image.open(reconstructName).convert('RGB'))
    # open the image file and get the RGBA data of the image
    # I_s  = (Image.open(reconstructName)).getdata()

    # convert the arrays to 1d arrays
    I_o = [[t[0] for t in inner_list] for inner_list in downscaled_array]


    # open a file for writing array values
    with open('new_list_output.txt', 'w') as file1:
        # iterate through the array and write each value to a new line in the file
        for value1 in I_o:
            file1.write(str(value1) + '\n')

    # open a file for writing values 2
    with open('output_array_output.txt', 'w') as file2:
        # iterate through the array and write each value to a new line in the file
        for value2 in I_s:
            file2.write(str(value2) + '\n')

    # print(downscaled_array)
    # print(origin_img)

    # print(f"Width: {mae_width}, Height: {mae_height}")
    # print(len(downscaled_array))
    # print(len(origin_img))

    # pass in width and height

    # I_o = np.array(downscaled_array)
    # I_s = np.array(output_array)
    # if I_o.shape != I_s.shape:
    #     raise ValueError("Arrays must have the same shape")
    h = len(I_s)
    w = 3
    # w, h = I_s.shape # Assuming both arrays have the same shape
    total_error = 0
    for i in range(w):
        for j in range(h):
            # if i >= w or j >= h:
            #     raise IndexError(f"Index ({i}, {j}) out of bounds for array")
            total_error += abs(I_o[i][j] - I_s[i][j])
    mae = total_error / (w * h)
    print(f'Our MAE is: {mae}')
'''




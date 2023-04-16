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

NOTE: this program will only work with square images in downscaling, otherwise you will get a distorted output!
'''

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Importing Libraries / Modules
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

import random
from PIL import Image
import numpy as np
import cv2

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

    # grab coefficients
    # SOURCE: https://www.geeksforgeeks.org/implementing-shamirs-secret-sharing-scheme-in-python/
    coefficients = [[random.randint(0, 250) for _ in range(r-1)] for _ in range(len(openedImageArray))]
    image_array_generated = []
    for i in range(1, n + 1):
        base = [i ** j for j in range(1, r)]
        imageList_ = []
        for p in range(len(openedImageArray)):
            base_sum = sum([coefficients[p][j] * base[j] for j in range(r-1)])
            imageList_.append((openedImageArray [p] + base_sum) % 251)
        image_array_generated.append(imageList_)


    ''' NON DOWNSCALING'''
    # Reconstruction data
    array_bits = image_array_generated[0:r]
    decode_list = list(range(1, r + 1))

    share_names = []
    # Create Share value images
    to_save = [Image.new("L", (width, height)) for _ in range(n)]
    for i, imgOut in enumerate(image_array_generated):
        to_save[i].putdata(imgOut)
        # name_of_share = "share{}.bmp".format(i + 1)
        # if downscaleBool == True
        name_of_share = f"share{i + 1}.bmp"
        to_save[i].save(name_of_share)
        share_names.append(name_of_share)

    new_array_boi = []
    # checks to see if downscaling is active
    if downscaleBool == True:
        '''DOWN SCALING'''
        print("Downscaling Activated!")
        for labels in share_names:
            new_width, new_height, new_array_boi = downscale_image(labels, width, height,labels)
            #new_width, new_height, new_array_boi = downscale_image_original(labels, width, height, labels)
        width = new_width
        height = new_height
        # array_bits = new_array_boi

    else:
        print("No Downscaling Requested!")


        print("Encrypted Shares Generated!")

    return image_array_generated,(width, height),array_bits,decode_list,new_array_boi

'''
# --- Downscale Image Method 1 ---
def downscale_image_original(orig_image, width, height, shareNo):
    print(f"Downscaling {shareNo} With PILLOW...")
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
'''


# --- Downscale Image Method 2 ---
# SOURCE: Image Resizing with OpenCV: https://learnopencv.com/image-resizing-with-opencv/
def downscale_image(inputImage, width_in, height_in,shareNo):
    print(f"Downscaling {shareNo} With OpenCV...")
    # print(f"Need to make the image: {(width_in//2)} by {(height_in//2)}")
    
    # needs to be black and white before using, but we have already taken care of that
    cvImageOriginal = cv2.imread(inputImage)

    # Get the dimensions of the image
    height, width, channels = cvImageOriginal.shape

    # Downsize the image by two
    half_height, half_width = int(height/2), int(width/2)

    # Create a new image with the downsampled dimensions
    downsampledcvImageOriginal = np.zeros((half_height, half_width, channels), dtype=np.uint8)

    new_array_pixel_values = []
    # Iterate over the downsampled image and average the neighboring pixels
    for i in range(half_height):
        for j in range(half_width):
            # Calculate the indices of the four neighboring pixels
            top_left = (i*2, j*2)
            top_right = (i*2, j*2+1)
            bottom_left = (i*2+1, j*2)
            bottom_right = (i*2+1, j*2+1)
            
            # Average the pixel values of the four neighbors and take modulo 251
            pixel_value = (cvImageOriginal[top_left] + cvImageOriginal[top_right] + cvImageOriginal[bottom_left] + cvImageOriginal[bottom_right]) // 4 % 251
            
            # Assign the new pixel value to the downsampled image
            downsampledcvImageOriginal[i, j] = pixel_value

            new_array_pixel_values.append(pixel_value)

    # Save the downsampled image to a file and return the values
    cv2.imwrite(inputImage, downsampledcvImageOriginal)
    # return half_width, half_height, new_array_pixel_values
    return half_width, half_height, downsampledcvImageOriginal #use the last value to get the MAE





# --- Function to reconstruct the secret using Lagrange function ---
# SOURCE: https://github.com/cfgnunes/numerical-methods-python/blob/main/interpolation.py
'''CHANGE THE VARIABLES - try subbing with above function'''
def lagrange_calc_shamir(x, y, number_of_points, use_this_X):
    setupArray = [0] * number_of_points
    lagrange_out = 0
    for k in range(number_of_points):
        setupArray[k] = 1
        for k_ in range(number_of_points):
            if k != k_:
                setupArray[k] = setupArray[k] * (use_this_X- x[k_]) / (x[k] - x[k_])
            else:
                pass
    for i in range(number_of_points):
        lagrange_out += y[i] * setupArray[i]

    # print("Lagrange Function Executed!") # TOO MANY PRINT OUTS
    return lagrange_out



# --- Function to reconstruct the original image using the shares ---
# SOURCE: https://www.geeksforgeeks.org/implementing-shamirs-secret-sharing-scheme-in-python/
'''CHANGE THE VARIALBES'''
def decrypt_image_shamir(input_image, list_values, r, n):
    # assert len(imgs) >= r
    # x = index
    length_of_image = len(input_image[0])
    image_pixel_array= []
    for i in range(length_of_image):
        y = [input_image[j][i] for j in range(r)]
        pixel = lagrange_calc_shamir(list_values, y, r, 0) % 251
        image_pixel_array.append(pixel)

    print("Decrypted Image Restored!")
    return image_pixel_array


# --- Function to decode downsized pics ---
''' # DO WE NEED TWO DOWNSIZE FUNCTIONS????
def decode_downsize(imgs, index, r, n):
    # # you can also just re open up the share by passing in the name and get the dimensions that way

    # Make sure there are enough shares to decode the image
    if len(imgs) < r:
        raise ValueError(f"Not enough shares to decode image (need {r}, got {len(imgs)})")
    
    # Calculate the width of the image
    # img_width = len(imgs[0]) // 2
    img_width = len(imgs[0])
    
    # Reconstruct the pixel values
    img = []
    # ITS RECONSTRUCTION!!!!
    # for col_idx in range(0,img_width,2):
    for col_idx in range(0,img_width):
        shares_to_use = [imgs[share_idx][col_idx] for share_idx in range(r)]
        pixel_value = shamir_lagrange_calc(index, shares_to_use, r, 0) % 251
        # print(f"Print Pixel: {pixel_value}")
        img.append(pixel_value)

    # cut array in half, then start again

    # get second half of pictures
    # for col_idx in range(1,img_width-1,2):
    #     shares_to_use = [imgs[share_idx][col_idx] for share_idx in range(r)]
    #     pixel_value = lagrange(index, shares_to_use, r, 0) % 251
    #     # print(f"Print Pixel: {pixel_value}")
    #     img.append(pixel_value)

    print("Image reconstruction complete!")
    return img
'''
# --- Function to crop output for MAE ---
# SOURCE: Cropping Images in Python With Pillow and OpenCV: https://cloudinary.com/guides/automatic-image-cropping/cropping-images-in-python-with-pillow-and-opencv
def crop_output(imageInput):
    # Open the image file
    image = Image.open(imageInput)

    # Get the current dimensions of the image
    current_width, current_height = image.size

    # Set the dimensions for cropping to the upper left quarter
    width = current_width // 2
    height = current_height // 2

    # Crop the image
    cropped_image = image.crop((0, 0, width, height))

    # Save the cropped image
    cropped_image.save(imageInput)


# --- Function to calculate the MAE ---
def calculate_mae(resized_image,initial_resized_array):
    print("Calculating MAE...")
    outputImageCv = cv2.imread(resized_image) 
    # outputImageCv = cv2.imread('image.png', cv2.IMREAD_UNCHANGED)
    if outputImageCv.shape != initial_resized_array.shape:
        outputImageCv.shape = cv2.resize(outputImageCv, initial_resized_array.shape[:2][::-1])

    # Calculate the absolute difference between the images
    diff = cv2.absdiff(outputImageCv, initial_resized_array)

    # Convert the difference image to grayscale
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    # Calculate the mean value of the grayscale image
    mae = np.mean(gray)

    print("Our Mean Average Error is:", mae)


# def calculate_mae(img1_path, img2_path):
#     # Load the images and convert them to numpy arrays
#     img1 = np.array(Image.open(img1_path).convert('L')) # convert to grayscale
#     img2 = np.array(Image.open(img2_path).convert('L'))

#     # Calculate the absolute difference between the pixel values of two images
#     diff = np.abs(img1 - img2)

#     # Calculate the sum of absolute differences and divide by the total number of pixels
#     mae = np.sum(diff) / (img1.shape[0] * img1.shape[1])
#     print(f"Mean Average Error between {img1_path} & {img2_path}: {mae}")

#     return mae

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
useThisImage = '3.bmp'
totalNumberOfShares = 5
minNumberOfShares = 3
wantDownscale = True


reconstructName = f"reconstructed_{useThisImage}"

'''ENCRYPTION'''
image_array_generated_output,shape,arr_bit,list_bit,downscaled_array_to_compare = split_image_shamir(useThisImage,wantDownscale,totalNumberOfShares,minNumberOfShares,max_value=250) # change r and n names
# print(f"Orig Shape: {shape}")
print('#------------#')

''' DECRYPTION'''
# NEED TO DO SEPERATE FUNCTION IF DOWNSCALING WAS REQUESTED
'''NO DOWNSCALE'''
if wantDownscale == False:
    origin_img = decrypt_image_shamir(arr_bit, list_bit, minNumberOfShares, totalNumberOfShares)
    # save output
    img = Image.new("L", shape, color=0)
    img.putdata(list(origin_img))
    img.save(reconstructName)
else:
    '''DOWNSCALE'''

    # origin_img = decode_downsize(arr_bit, list_bit, minNumberOfShares, totalNumberOfShares)
    origin_img = decrypt_image_shamir(arr_bit, list_bit, minNumberOfShares, totalNumberOfShares)
    # Save the decrypted image to a file

    # pass in width and height
    # save output (width and height half) -- get it from the start of the project
    half_values_array = origin_img[::2] # Get every second element starting from the first
    # half_values_array = origin_img[::4]
    # print(f"Length of List: {len(list(origin_img))}")
    # print(f"Output Array is {len(origin_img)}")
    # print(f"Expecting Array that is {shape[0]*shape[1]}")
    # print(f"half values array has {len(half_values_array)}")

    # newShapeDim = (len(half_values_array)+54)//320
    newShapeDim = (len(half_values_array))//320
    newShape = ((newShapeDim),(newShapeDim)) # only works with square shapes
    # print(newShape)

    img = Image.new("L", newShape, color=0)

    img.putdata(list(half_values_array))
    img.save(f"{shape[1]}x{shape[0]}_{reconstructName}")
    crop_output(f"{shape[1]}x{shape[0]}_{reconstructName}")
    print('#------------#')
    # --- MAE ---
    # uses original number array returned from downsize and then opens up output image to compare against
    # ASK PRADEEP IF YOU ARE DOING THIS RIGHT!!
    calculate_mae(f"{shape[1]}x{shape[0]}_{reconstructName}",downscaled_array_to_compare)


    # for i in range(totalNumberOfShares):
    #     # shareName = f'downsized_share{i+1}.bmp'
    #     shareName = f'share{i+1}.bmp'
    #     ourMae = calculate_mae(f"{shape[1]}x{shape[0]}_{reconstructName}",shareName)

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




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
    imageOpened = Image.open(inputImage).convert('L')
    openedImageArray = []
    width, height = imageOpened.size
    for y in range(height):
        for x in range(width):
            pixel = imageOpened.getpixel((x, y))
            if max_value is not None:
                pixel = min(pixel, max_value)
            openedImageArray.append(pixel)

    # grab coefficients
    # SOURCE: https://www.geeksforgeeks.org/implementing-shamirs-secret-sharing-scheme-in-python/
    coefficients = [[random.randint(0, 250) for _ in range(r-1)] for _ in range(len(openedImageArray))]
    image_array_generated = []
    for i in range(1, n + 1):
        initial = [i ** j for j in range(1, r)]
        imageList_ = []
        for p in range(len(openedImageArray)):
            sum_initial = sum([coefficients[p][j] * initial[j] for j in range(r-1)])
            imageList_.append((openedImageArray [p] + sum_initial) % 251)
        image_array_generated.append(imageList_)


    ''' NON DOWNSCALING'''
    # Reconstruction data
    array_bits = image_array_generated[0:r]
    decode_list = list(range(1, r + 1))

    share_names = []
    # Create Share value images
    output_this = [Image.new("L", (width, height)) for _ in range(n)]
    for i, image_Out in enumerate(image_array_generated):
        output_this[i].putdata(image_Out)
        # name_of_share = "share{}.bmp".format(i + 1)
        name_of_share = f"share{i + 1}.bmp"
        output_this[i].save(name_of_share)
        share_names.append(name_of_share)

    new_array_boi = []
    # checks to see if downscaling is active
    if downscaleBool == True:
        '''DOWN SCALING'''
        print("Downscaling Activated!")
        for labels in share_names:
            new_width, new_height, new_array_boi = downscale_image(labels, width, height,labels)
        width = new_width
        height = new_height
        # array_bits = new_array_boi

    else:
        print("No Downscaling Requested!")


        print("Encrypted Shares Generated!")

    return image_array_generated,(width, height),array_bits,decode_list,new_array_boi



# --- Downscale Image Method 2 ---
# SOURCE: Image Resizing with OpenCV: https://learnopencv.com/image-resizing-with-opencv/
def downscale_image(inputImage, width_in, height_in,shareNo):
    print(f"Downscaling {shareNo} With OpenCV...")
    # print(f"Need to make the image: {(width_in//2)} by {(height_in//2)}")
    cvImageOriginal = cv2.imread(inputImage) # needs to be black and white before using, but we have already taken care of that
    height, width, channels = cvImageOriginal.shape
    half_height, half_width = int(height/2), int(width/2) # get the new dimensions for output image
    downsampledcvImageOriginal = np.zeros((half_height, half_width, channels), dtype=np.uint8) # create new image, using new dimensions
    # new_array_pixel_values = []
    # average x4 pixels by going through them
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

            # new_array_pixel_values.append(pixel_value)

    # Save the downsampled image to a file and return the values
    cv2.imwrite(inputImage, downsampledcvImageOriginal)
    return half_width, half_height, downsampledcvImageOriginal #use the last value to get the MAE



# --- Function to reconstruct the secret using Lagrange function ---
# SOURCE: https://github.com/cfgnunes/numerical-methods-python/blob/main/interpolation.py
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
def decrypt_image_shamir(input_image, list_values, r, n):
    length_of_image = len(input_image[0])
    image_pixel_array= []
    for i in range(length_of_image):
        y = [input_image[j][i] for j in range(r)]
        pixel = lagrange_calc_shamir(list_values, y, r, 0) % 251
        image_pixel_array.append(pixel)

    print("Decrypted Image Restored!")
    return image_pixel_array



# --- Function to crop output for MAE ---
# SOURCE: Cropping Images in Python With Pillow and OpenCV: https://cloudinary.com/guides/automatic-image-cropping/cropping-images-in-python-with-pillow-and-opencv
def crop_output(imageInput):
    image = Image.open(imageInput) # Open the image and get current dimensions
    current_width, current_height = image.size
    width = current_width // 2 # Set the dimensions for cropping to the upper left quarter & crop
    height = current_height // 2
    cropped_image = image.crop((0, 0, width, height))
    cropped_image.save(imageInput)# Save the cropped image



# --- Function to calculate our MAE ---
def calc_mae_numpy(inputImage, pixelArrayValues):
    outputImage = cv2.imread(inputImage) # read image in from file
    outputImageCv = outputImage.flatten()
    pixelArrayValues = np.array(pixelArrayValues) # added to see if this will more accurately look at mae
    pixelArrayValuesFlatten = pixelArrayValues.flatten()
    outputMAE = np.mean(np.abs(outputImageCv - pixelArrayValuesFlatten)) # use formula to find the 
    print(f"Output MAE: {outputMAE}")
    return outputMAE



    # outputImageCv = cv2.imread(inputImage) # read image in from file
    # pixelArrayValues = np.array(pixelArrayValues) # added to see if this will more accurately look at mae
    # outputMAE = np.mean(np.abs(outputImageCv - pixelArrayValues)) # use formula to find the 
    # print(f"Output MAE: {outputMAE}")
    # return outputMAE



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

myLogo()
print("\n")

# LET THE USER SET THESE with input
# useThisImage = '3.bmp'
# totalNumberOfShares = 5
# minNumberOfShares = 3
# wantDownscale = True

totalNumberOfShares = 5
minNumberOfShares = 3
useThisImage = input("Enter in your input bitmap name (with extension): ") # input image name
reconstructName = f"reconstructed_{useThisImage}" # output image name

wantDownscale = True
wantDownscaleString = input("Do you want to downscale? (yes or no): ")
wantDownscaleString = wantDownscaleString.lower()
# Set the downscale boolean variable based on the user's response
if wantDownscaleString == "yes":
    wantDownscale = True
else:
    wantDownscale = False
# print(f"Downscale = {wantDownscale}")
print('\n')

'''ENCRYPTION'''
image_array_generated_output,shape,arr_bit,list_bit,downscaled_array_to_compare = split_image_shamir(useThisImage,wantDownscale,totalNumberOfShares,minNumberOfShares,max_value=250) 
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
    img.save(f"{shape[1]}x{shape[0]}_{reconstructName}")
else:
    '''DOWNSCALE'''
    origin_img = decrypt_image_shamir(arr_bit, list_bit, minNumberOfShares, totalNumberOfShares)

    # pass in width and height, save output (width and height half) -- get it from the start of the project
    half_values_array = origin_img[::2] # Get every second element starting from the first
    newShapeDim = (len(half_values_array))//320
    newShape = ((newShapeDim),(newShapeDim)) # only works with square shapes
    # above is neccessary because we were getting too much info from the array, x2 number pixels
    # every second number seemed to be a duplicate

    img = Image.new("L", newShape, color=0) # save downscaled image with these dimensions
    img.putdata(list(half_values_array))
    img.save(f"{shape[1]}x{shape[0]}_{reconstructName}")
    crop_output(f"{shape[1]}x{shape[0]}_{reconstructName}")
    print('#------------#')



    ''' CALC MAE '''
    # uses original number array returned from downsize and then opens up output image to compare against
    # ASK PRADEEP IF YOU ARE DOING THIS RIGHT!!
    calc_mae_numpy(f"{shape[1]}x{shape[0]}_{reconstructName}",downscaled_array_to_compare)
    # As MAE was only specified to be done for question 2, i did not include it for question 1



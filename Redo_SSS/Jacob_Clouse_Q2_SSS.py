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
import numpy as np
import random
from PIL import Image
# import sys


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Functions
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

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



# --- Function to split an image into shares using Shamir's Secret Sharing algorithm --- 
def split_image_shamir(imageToEncrypt, requiredNumberShares, totalGenShares):
    # Load the image, convert to grayscale just to be sure...
    with Image.open(imageToEncrypt).convert('L') as youBoiImage:
        dataArray = np.array(youBoiImage)
    # return img_array.flatten(), img_array.shape
    flat_boi = dataArray.flatten() # merge into single array
    image_dimensions = dataArray.shape # ie should be like "640x480"
    num_pix = (dataArray.flatten()).shape[0]

    print(f"Your original image is {image_dimensions}")
    print(f"You will create {totalGenShares} total")
    print(f"You will need {requiredNumberShares} to retrieve")
    print(f"Number of pixels: {num_pix}")


    num_pixels = num_pix # Get the total number of pixels in the image
    coef = np.random.randint(low = 0, high = 251, size = (num_pixels, requiredNumberShares - 1)) # Generate an array of random coefficients for the polynomial function
    gen_imgs = []
    for i in range(1, totalGenShares + 1):
        base = np.array([i ** j for j in range(1, requiredNumberShares)]) # Generate the base for the polynomial function
        base = np.matmul(coef, base) # Multiply the coefficients with the base to generate the shares
        img_ = flat_boi + base # Add the shares to the original image
        img_ = img_ % 251 # Take the modulo to ensure values are within the range [0, 250]
        gen_imgs.append(img_)


    '''THIS CODE NEEDS TO CHANGE!!!'''

    coeffConverted = np.array(gen_imgs) # redo and merge with below
    encryptedShares = coeffConverted.reshape(requiredNumberShares, *image_dimensions)
    for i, outputImage in enumerate(encryptedShares):
        Image.fromarray(outputImage.astype(np.uint8)).save("share_{}.bmp".format(i + 1))





'''
    # THIS IS NOT WORKING CORRECTLY ---
    # Split the image data into k shares using Shamir's Secret Sharing algorithm
    x_values = list(range(1, n+1))
    y_values = [img_data[i::3] for i in range(3)]
    shares = []
    for y in y_values:
        coeffs = [random.randint(1, 255) for i in range(k-1)]
        coeffs.insert(0, int.from_bytes(y, byteorder='big'))
        share = [(x, sum(c * x**i for i, c in enumerate(coeffs)) % 256) for x in x_values]
        shares.append(share)

    # Save each share as a separate BMP image file
    for i, share in enumerate(shares):
        img_share_data = np.zeros_like(img_data)
        for j, (x, y) in enumerate(share):
            img_share_data[j::n*3] = y
        img_share_bytes = header + bytes(img_share_data)
        with open(f"image_share_{i}.bmp", "wb") as f:
            f.write(img_share_bytes)
'''





# # --- Function to generate shares ---
# # SOURCE: https://www.geeksforgeeks.org/implementing-shamirs-secret-sharing-scheme-in-python/#
# def generate_shares(secret, n, k):
#     """
#     Generate n shares of the secret using a 2-out-of-n Shamir Secret Sharing scheme,
#     where any k shares can be used to reconstruct the secret.
#     Returns a list of tuples, where each tuple is a share in the form (x, y).
#     """
#     if k > n:
#         raise ValueError("k must be less than or equal to n")
    
#     coefficients = [secret] + [random.randint(1, 2**32-1) for _ in range(k-1)]
#     shares = []
#     for i in range(n):
#         x = i + 1
#         y = sum([coefficients[j] * x**j for j in range(k)])
#         shares.append((x, y))
#     return shares



# # --- Function to get shares and put them back together ---
# # SOURCE: https://www.geeksforgeeks.org/implementing-shamirs-secret-sharing-scheme-in-python/#
# def reconstruct_secret(shares):
#     """
#     Reconstruct the secret from a list of shares using Lagrange interpolation.
#     Returns the reconstructed secret.
#     """
#     if len(shares) < 2:
#         raise ValueError("At least 2 shares are required to reconstruct the secret")
#     x_values, y_values = zip(*shares)
#     secret = 0
#     for i in range(len(shares)):
#         numerator, denominator = 1, 1
#         for j in range(len(shares)):
#             if i != j:
#                 numerator *= -x_values[j]
#                 denominator *= (x_values[i] - x_values[j])
#         secret += y_values[i] * numerator // denominator
#     return secret


# # --- Function to save shares as bitmaps ---
# def save_shares_as_bitmaps(shares, header_data):
#     for i, share in enumerate(shares):
#         x, y = share
#         binary_data = format(y, "08b") # convert the y value to a binary string
#         byte_data = [int(binary_data[i:i+8], 2) for i in range(0, len(binary_data), 8)] # split the binary string into bytes
#         share_data = bytearray(byte_data) # convert the bytes to a bytearray
        
#         # # update the header information with the share data length
#         # share_size = len(share_data)
#         # header_data = header_data[:2] + share_size.to_bytes(4, byteorder="little") + header_data[10:]

#         # create a new bitmap file for the share
#         share_path = f"share_{i+1}.bmp"
#         with open(share_path, "wb") as f:
#             f.write(header_data)
#             f.write(share_data)



# # --- Function open the image and get shares --- #
# def encrypt_image(image_path, n, k):
#     """
#     Encrypt an image using Shamir Secret Sharing.
#     Returns a list of n shares.
#     """
#     with open(image_path, "rb") as f:
#         header_data = f.read(54) # read the bitmap header information
#         image_data = f.read()
#     # print(image_data)
#     binary_data = "".join(format(byte, "08b") for byte in image_data)
#     # go through each and every byte other than data and if its greater than 
#     # print(binary_data)
#     shares = generate_shares(int(binary_data, 2), n, k)
#     return shares,header_data




# # --- Function open shares and get tuples back --- #
# def read_shares_from_bitmaps(num_shares):
#     shares = []
#     for i in range(1, num_shares+1):
#         share_path = f"share_{i}.bmp"
#         with open(share_path, "rb") as f:
#             # skip the header information
#             f.seek(54)
#             share_data = f.read()

#         # convert the share data to a binary string
#         binary_data = "".join(format(byte, "08b") for byte in share_data)
#         # convert the binary string to an integer
#         y = int(binary_data, 2)
#         x = i
#         shares.append((x, y))

#     return shares




# # --- Function open the shares and return the image --- #
# def decrypt_image(bitmap_shares):
#     """
#     Decrypt an image using Shamir Secret Sharing.
#     Returns the decrypted image data as a bytes object.
#     """
#     secret = reconstruct_secret(bitmap_shares)
#     binary_data = bin(secret)[2:]
#     padding = 8 - len(binary_data) % 8
#     binary_data = "0" * padding + binary_data
#     bytes_data = bytes(int(binary_data[i:i+8], 2) for i in range(0, len(binary_data), 8))
#     return bytes_data


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

max_250(inputImage,new250Image)
split_image_shamir(new250Image, requiredSharesToRetrieve, totalNumberOfShares)












'''
# header_data, image_data = split_image_shamir(inputImage)

sys.set_int_max_str_digits(1000000)

# Encrypt the image
shares_stuff,header_stuff = encrypt_image(new250Image, n, k)
# print(shares)


# # open a file for writing tuple info
# with open('my_shares_output.txt', 'w') as f:
#     # iterate over the list and write each item to the file
#     for tuple1 in shares_stuff:
#         f.write(str(tuple1) + '\n\n\n')
save_shares_as_bitmaps(shares_stuff,header_stuff)



# Decrypt the image
shares_from_bitmaps = read_shares_from_bitmaps(2)
decrypted_data = decrypt_image(shares_from_bitmaps)

# Save the decrypted image to a file
with open("decrypted_image.bmp", "wb") as f:
    f.write(header_stuff + decrypted_data)

print("It worked!")

# 1 - get it so that the header info is opened as well in the data
# 2 - look at the decrypt data and the save data and then append the new data to the shares,
# 3 - try opening the shares, split off the header, recombine and decrypted, save with new header
'''

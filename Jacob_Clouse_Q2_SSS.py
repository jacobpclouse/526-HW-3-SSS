# This Python Program was written on Linux Mint and Windows 10 using VScode, your milage may vary on OS and configuration.

# **NOTES:**
# --- if we have probs with downscaling and images not having the correct number of pixels, we could potentally just scale them up to a power of 100 and then downscale them, it will work, need to talk with pradeep about this
# OR we can just have a check to make sure that there are a x4 values in each comparision beforehand, and IF NOT it will just fill take the original value and use that
# **** OOORRR we can get the pixel count first, mod 4 it and (if remainder exists), add extra pixel values, then group and average them


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Importing Libraries / Modules 
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
import random
from PIL import Image



# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Variables
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-



# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Functions
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# --- Function to read in an image --- DO NOT USE
# SOURCE: https://www.geeksforgeeks.org/reading-images-in-python/




# --- Function to generate shares ---
# SOURCE: https://www.geeksforgeeks.org/implementing-shamirs-secret-sharing-scheme-in-python/#
def generate_shares(secret, n, k):
    """
    Generate n shares of the secret using a 2-out-of-n Shamir Secret Sharing scheme,
    where any k shares can be used to reconstruct the secret.
    Returns a list of tuples, where each tuple is a share in the form (x, y).
    """
    if k > n:
        raise ValueError("k must be less than or equal to n")
    coefficients = [secret] + [random.randint(1, 2**32-1) for _ in range(k-1)]
    shares = []
    for i in range(n):
        x = i + 1
        y = sum([coefficients[j] * x**j for j in range(k)])
        shares.append((x, y))
    return shares



# --- Function to get shares and put them back together ---
# SOURCE: https://www.geeksforgeeks.org/implementing-shamirs-secret-sharing-scheme-in-python/#
def reconstruct_secret(shares):
    """
    Reconstruct the secret from a list of shares using Lagrange interpolation.
    Returns the reconstructed secret.
    """
    if len(shares) < 2:
        raise ValueError("At least 2 shares are required to reconstruct the secret")
    x_values, y_values = zip(*shares)
    secret = 0
    for i in range(len(shares)):
        numerator, denominator = 1, 1
        for j in range(len(shares)):
            if i != j:
                numerator *= -x_values[j]
                denominator *= (x_values[i] - x_values[j])
        secret += y_values[i] * numerator // denominator
    return secret







# --- Function open the image and get shares --- #
def encrypt_image(image_path, n, k):
    """
    Encrypt an image using Shamir Secret Sharing.
    Returns a list of n shares.
    """
    with open(image_path, "rb") as f:
        image_data = f.read()
    binary_data = "".join(format(byte, "08b") for byte in image_data)
    shares = generate_shares(int(binary_data, 2), n, k)
    return shares


# --- Function open the shares and return the image --- #
def decrypt_image(shares):
    """
    Decrypt an image using Shamir Secret Sharing.
    Returns the decrypted image data as a bytes object.
    """
    secret = reconstruct_secret(shares)
    binary_data = bin(secret)[2:]
    padding = 8 - len(binary_data) % 8
    binary_data = "0" * padding + binary_data
    bytes_data = bytes(int(binary_data[i:i+8], 2) for i in range(0, len(binary_data), 8))
    return bytes_data

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

inputImage = 'bitmap_guts.bmp'
n = 5
k = 2

# Encrypt the image
shares = encrypt_image(inputImage, n, k)

# Decrypt the image
decrypted_data = decrypt_image(shares)

# Save the decrypted image to a file
with open("decrypted_image.bmp", "wb") as f:
    f.write(decrypted_data)

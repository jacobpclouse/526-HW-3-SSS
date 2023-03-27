# This Python Program was written on Linux Mint and Windows 10 using VScode, your milage may vary on OS and configuration.

# **NOTES:**
# --- if we have probs with downscaling and images not having the correct number of pixels, we could potentally just scale them up to a power of 100 and then downscale them, it will work, need to talk with pradeep about this
# OR we can just have a check to make sure that there are a x4 values in each comparision beforehand, and IF NOT it will just fill take the original value and use that



# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Importing Libraries / Modules 
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

from PIL import Image # used to read in an image

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Functions
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# --- Function read in an image --- DO NOT USE
# SOURCE: https://www.geeksforgeeks.org/reading-images-in-python/
def readInImage(ImageToRead):
    print(f"Reading Image: {ImageToRead}")
    # Read image
    imgInComputer = Image.open(ImageToRead)
    # Output Images
    imgInComputer.show()
    # prints format of image
    print(imgInComputer.format)
    # prints mode of image
    print(imgInComputer.mode)
    # returning the value to output - 
    return imgInComputer



# --- Function downscale the image ---
def downscaleImage(InputImageName):
    print(f"* ---- Reading Image: {InputImageName} ---- *")
    # Read image - PIL Library
    imageReadInComputer = Image.open(InputImageName)
    # Get Image Size / Dimensions
    imageWidth, imageHeight = imageReadInComputer.size

    # Get Pixel Data
    imageNumPixels = imageWidth * imageHeight
    imagePixels = list(imageReadInComputer.getdata()) # this is too large to print, fills screen 
    

    print(f"Original Width: {imageWidth}")
    print(f"Original Height: {imageHeight}")
    print(f"Original # of Pixels (WIDTH x HEIGHT): {imageNumPixels}")
    # print(f"Original Pixel Values: {imagePixels}")

    # save pixel values to text file - analyze
    # save_String(imagePixels,f'{InputImageName}_ImagePixelValues')


    print(f"* ---- Downscaling: {InputImageName}  ---- *")


# --- Function to save string to file  ---
def save_String(textValues, nameOfFile):
    print(type(textValues))
    if type(textValues) == list:
        with open(f"{nameOfFile}_List.txt", "w") as text_file:
            for item in textValues:
                text_file.write(str(item) + "\n")
    elif type(textValues) == str:
        with open(f"{nameOfFile}_Str.txt", "w") as text_file:
            text_file.write(textValues)




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

inputImage = 'bitmap_guts.bmp'
# outputImage = readInImage(inputImage)
downscaleImage(inputImage)


myLogo()
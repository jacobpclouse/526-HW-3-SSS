# This Python Program was written on Linux Mint and Windows 10 using VScode, your milage may vary on OS and configuration.

# **NOTES:**
# --- if we have probs with downscaling and images not having the correct number of pixels, we could potentally just scale them up to a power of 100 and then downscale them, it will work, need to talk with pradeep about this
# OR we can just have a check to make sure that there are a x4 values in each comparision beforehand, and IF NOT it will just fill take the original value and use that
# **** OOORRR we can get the pixel count first, mod 4 it and (if remainder exists), add extra pixel values, then group and average them


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
    # imageReadInComputer = Image.open(InputImageName)
    imageReadInComputer = Image.open(InputImageName).convert('RGB')

    # Get Image Size / Dimensions
    imageWidth, imageHeight = imageReadInComputer.size

    # Get Pixel Data
    imageNumPixels = imageWidth * imageHeight
    imagePixels = list(imageReadInComputer.getdata()) # this is too large to print, fills screen 
    

    print(f"Original Width: {imageWidth}")
    print(f"Original Height: {imageHeight}")
    print(f"Original # of Pixels (WIDTH x HEIGHT): {imageNumPixels}")
    # print(f"Original Pixel Values: {imagePixels}") # this is too large to print, fills screen 

    # save pixel values to text file - analyze
    # save_String(imagePixels,f'{InputImageName}_ImagePixelValues') 


    print(f"* ---- Downscaling: {InputImageName}  ---- *")
    # get mod 4 of pixel values 
    IsThereRemainder = imageNumPixels % 4
    print(f"Remainder: {IsThereRemainder}")
    if IsThereRemainder != 0:
        needToAdd = (4 - IsThereRemainder)
        print(f"Need to add: {needToAdd}")

# REDO FOLLOWING: ---------
    # convertedImage = Image.open(InputImageName).convert('RGB')

    # Calculate the size of the output image
    newWidth = imageWidth // 2
    newHeight = imageHeight // 2

    # Create a new image with the calculated size
    outputImage = Image.new('RGB', (newWidth, newHeight))

    # Loop through each pixel of the output image
    for x in range(newWidth):
        for y in range(newHeight):
            
            # Calculate the average of the four pixels in the input image
            r = g = b = 0
            for i in range(2):
                for j in range(2):
                    px = imageReadInComputer.getpixel((2*x+i, 2*y+j))
                    r += px[0]
                    g += px[1]
                    b += px[2]
            r //= 4
            g //= 4
            b //= 4
            
            # Set the pixel value in the output image
            outputImage.putpixel((x, y), (r, g, b))

    # Save the output image
    outputImage.save('output_image.jpg')

    # END REDO SECTION: -----


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

myLogo()

inputImage = 'bitmap_guts.bmp'
# outputImage = readInImage(inputImage)
downscaleImage(inputImage)



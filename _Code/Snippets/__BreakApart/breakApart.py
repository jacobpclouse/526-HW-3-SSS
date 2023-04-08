# Open the original bitmap image file
with open("1max250.bmp", "rb") as f:
    data = f.read()

# Extract the header from the file data
header = data[:54]

# Extract the image data from the file data
image_data = data[54:]

# Split the image data in half
half_len = len(image_data) // 2
image_data_1 = image_data[:half_len]
image_data_2 = image_data[half_len:]

# Create two new bitmap image files
with open("new1.bmp", "wb") as f1, open("new2.bmp", "wb") as f2:
    # Combine the first block of image data with the header of the first new file
    f1.write(header + image_data_1)
    
    # Combine the second block of image data with the header of the second new file
    f2.write(header + image_data_2)

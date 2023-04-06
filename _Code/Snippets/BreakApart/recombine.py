# Open the first bitmap image file
with open("new1.bmp", "rb") as f1:
    data1 = f1.read()

# Open the second bitmap image file
with open("new2.bmp", "rb") as f2:
    data2 = f2.read()

# Extract the header from the first bitmap image file
header = data1[:54]

# Combine the image data from both files
combined_image_data = data1[54:] + data2[54:]

# Create a new bitmap image file with the combined header and image data
with open("combined.bmp", "wb") as f:
    f.write(header + combined_image_data)

import numpy as np
import random
import struct

def split_image(image_path, k=2, n=5):
    with open(image_path, 'rb') as f:
        # Read the header of the BMP file format (first 54 bytes)
        header = f.read(54)
        # Read the image data into a numpy array
        image = np.fromfile(f, dtype=np.uint8)
    
    # Calculate the size of each share
    share_size = int(len(image) / k)
    
    # Create empty arrays for the shares
    shares = [np.zeros(len(image), dtype=np.uint8) for i in range(n)]
    
    # Generate random coefficients for the polynomial
    coeffs = [random.randint(1, 255) for i in range(k)]
    
    # Split the image into shares
    for i in range(len(image)):
        # Evaluate the polynomial for each share
        for j in range(n):
            x = j + 1
            y = sum([coeffs[m] * x**m for m in range(k)])
            shares[j][i] = y ^ image[i]
    
    # Write the shares to files
    for i in range(n):
        share_path = image_path + '.share' + str(i)
        with open(share_path, 'wb') as f:
            # Write the header of the BMP file format (first 54 bytes)
            f.write(header)
            # Write the share data to the file
            shares[i].tofile(f)
            
    return coeffs,header

def reconstruct_image(image_path, coeffs, share_indices,header):
    # Read the shares into numpy arrays
    shares = []
    for i in share_indices:
        share_path = image_path + '.share' + str(i)
        with open(share_path, 'rb') as f:
            # Read the header of the BMP file format (first 54 bytes)
            f.read(54)
            # Read the share data into a numpy array
            share = np.fromfile(f, dtype=np.uint8)
            shares.append(share)
    
    # Calculate the size of the reconstructed image
    image_size = len(shares[0])
    
    # Create an empty array for the reconstructed image
    image = np.zeros(image_size, dtype=np.uint8)
    
    # Reconstruct the image from the shares
    for i in range(image_size):
        x_values = [j + 1 for j in share_indices]
        y_values = [shares[j][i] for j in share_indices]
        y = 0
        for j in range(len(x_values)):
            term = y_values[j]
            for k in range(len(x_values)):
                if k != j:
                    term = term * (0 - x_values[k]) / (x_values[j] - x_values[k])
            y += term
        image[i] = y ^ sum([coeffs[m] * (i + 1)**m for m in range(len(coeffs))])
    
    # Write the reconstructed image to a file
    reconstructed_image_path = image_path + '.reconstructed'
    with open(reconstructed_image_path, 'wb') as f:
        # Write the header of the BMP file format (first 54 bytes)
        f.write(header)
        # Write the reconstructed image data to the file
        image.tofile(f)


# Split the image into shares
coeffs,my_header = split_image('1.bmp', k=2, n=5)

# Reconstruct the image using shares 1 and 3
reconstruct_image('1.bmp', coeffs, [1, 3],my_header)


import numpy as np
import cv2

def split_image(filename):
    # Read image file and extract pixel data
    img = cv2.imread(filename)
    pixel_data = np.array(img[:, :, :])

    # Split pixel data into 5 equal parts
    split_data = np.array_split(pixel_data, 5)

    # Generate random polynomials for each share
    share_polynomials = []
    for i in range(5):
        coefficients = np.random.randint(0, 255, size=(2,))
        coefficients[0] = split_data[i][0]  # Extract single element from array
        share_polynomials.append(np.poly1d(coefficients))

    # Evaluate polynomials for x-values 1-5 to get share values
    shares = []
    for i in range(5):
        share_values = []
        for j in range(1, 6):
            share_values.append(share_polynomials[i](j))
        shares.append((i+1, np.array(share_values)))

    # Store shares in separate files or database
    for i in range(5):
        share_filename = f'share_{i+1}.npy'
        np.save(share_filename, shares[i])

def reconstruct_image(shares):
    # Extract x and y values from two shares
    x1, y1 = shares[0]
    x2, y2 = shares[1]

    # Use Lagrange interpolation to find polynomial coefficients
    lagrange_coeffs = np.polyfit([x1, x2], [y1, y2], deg=1)

    # Evaluate polynomial for pixel data
    pixel_data = np.polyval(lagrange_coeffs, range(54))

    # Reshape pixel data and save reconstructed image
    reconstructed_img = np.reshape(pixel_data, (54, -1, 3))
    cv2.imwrite('reconstructed_image.bmp', reconstructed_img)

# Example usage
split_image('1.bmp')
share1 = np.load('share_1.npy')
share3 = np.load('share_3.npy')
reconstruct_image([share1, share3])

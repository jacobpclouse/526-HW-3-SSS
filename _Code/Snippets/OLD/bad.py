import numpy as np
from PIL import Image

# Read the BMP image file
img = Image.open("1.bmp")

# Extract pixel data from the image
img_data = np.array(img)

# Set the parameters for Shamir's Secret Sharing Scheme
k = 3  # minimum number of shares required to reconstruct the secret
n = 5  # total number of shares

# Generate random coefficients for the polynomial of degree k-1
coefficients = np.random.randint(0, 256, size=k-1)

# Generate n shares using Shamir's Secret Sharing Scheme
shares = []
for i in range(1, n+1):
    x = i
    y = np.sum(coefficients * (x**np.arange(k-1))) + img_data[x-1][y-54]
    shares.append((x, y))

# Save the shares as separate image files
for i in range(n):
    share_img = Image.new("L", img.size)
    share_img.putdata(shares[i][1])
    share_img.save(f"share{i}.bmp")

# Choose any k shares and reconstruct the original pixel data
chosen_shares = np.random.choice(shares, size=k, replace=False)
chosen_x = [share[0] for share in chosen_shares]
chosen_y = [share[1] for share in chosen_shares]

# Use Lagrange interpolation to obtain the original pixel data
original_data = []
for x in range(img_data.shape[0]):
    row = []
    for y in range(img_data.shape[1]):
        row.append(int(np.sum([chosen_y[i] * np.prod([x - chosen_x[j] if j != i else 1 for j in range(k)]) * np.prod([1/(chosen_x[i] - chosen_x[j]) if j != i else 1 for j in range(k)]) for i in range(k)])))
    original_data.append(row)

# Save the reconstructed image as a BMP file
reconstructed_img = Image.fromarray(np.array(original_data).astype(np.uint8))
reconstructed_img.save("reconstructed_image.bmp")

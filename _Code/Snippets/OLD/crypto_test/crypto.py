import numpy as np
from PIL import Image
from Crypto.Util import number

def split_secret(secret, n, k):
    coeffs = [secret] + [number.getRandomRange(0, 255) for _ in range(k-1)]
    shares = []
    for i in range(n):
        x = i + 1
        y = sum(c * x**j for j, c in enumerate(coeffs))
        shares.append((x, y))
    return shares

def interpolate(shares, k):
    xs, ys = zip(*shares[:k])
    coeffs = np.polyfit(xs, ys, k-1)
    return coeffs

def reconstruct(shares, coeffs):
    xs, ys = zip(*shares)
    secret = np.zeros_like(ys[0])
    for c, coeff in enumerate(coeffs):
        secret += coeff * np.array(xs)**c
    return secret

# Load the image
img = Image.open('logo.png')

# Convert the image to a numpy array
img_array = np.asarray(img)

# Split the image into shares
shares = split_secret(img_array, 5, 3)

# Save the shares to files
for i, (x, y) in enumerate(shares):
    np.savetxt(f'share{i}.txt', np.array([x, y]), fmt='%d')

# Reconstruct the secret from the shares
coeffs = interpolate(shares, 3)
secret_array = reconstruct(shares, coeffs)

# Convert the secret array back to an image
secret_img = Image.fromarray(secret_array.astype('uint8'), mode='RGB')

# Save the secret image to a file
secret_img.save('reconstructed_image.png')

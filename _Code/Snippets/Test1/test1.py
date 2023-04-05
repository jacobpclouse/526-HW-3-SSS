import numpy as np
import random
from PIL import Image

# Function to split an image into shares using Shamir's Secret Sharing algorithm
def split_image_shamir(image_path, k, n):
    # Load the image
    with open(image_path, "rb") as f:
        header = f.read(54) # BMP header is 54 bytes long
        img_bytes = f.read()
    img_data = np.frombuffer(img_bytes, dtype=np.uint8)

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

# Function to reconstruct an image from shares using Shamir's Secret Sharing algorithm
def reconstruct_image_shamir(image_share_paths):
    # Load the shares
    shares = []
    for image_share_path in image_share_paths:
        with open(image_share_path, "rb") as f:
            header = f.read(54)
            img_share_bytes = f.read()
        img_share_data = np.frombuffer(img_share_bytes, dtype=np.uint8)
        shares.append([(i+1, img_share_data[i::3][0]) for i in range(len(img_share_data)//3)])

    # Combine the shares using Shamir's Secret Sharing algorithm to reconstruct the original image
    n = len(shares)
    k = len(shares[0])
    img_data = np.zeros(k*n*3, dtype=np.uint8)
    for i in range(k):
        for j in range(n):
            x_j, y_j = shares[j][i]
            p_j = 1
            for m in range(n):
                if m != j:
                    x_m, y_m = shares[m][i]
                    p_j = (p_j * (0 - x_m) * pow(x_j - x_m, -1, 256)) % 256
            img_data[i*n*3 + j*3 + 0] = y_j
            img_data[i*n*3 + j*3 + 1] = 0
            img_data[i*n*3 + j*3 + 2] = 0
    img_bytes = header + bytes(img_data)
    with open("reonstructed_image.bmp", "wb") as f:
        f.write(img_bytes)


# ---
#split_image_shamir("1.bmp", 2, 3)

reconstruct_image_shamir(["image_share_0.bmp", "image_share_1.bmp"])



'''
Error: (thinks its because its not 251, need to adjust):
----
Traceback (most recent call last):
  File "test1.py", line 66, in <module>
    reconstruct_image_shamir(["image_share_0.bmp", "image_share_1.bmp"])
  File "test1.py", line 54, in reconstruct_image_shamir
    p_j = (p_j * (0 - x_m) * pow(x_j - x_m, -1, 256)) % 256
ValueError: base is not invertible for the given modulus



'''
import random
from PIL import Image

def generate_shares(secret_image_path, n, k):
    """
    Generate n shares of the secret image using a 2-out-of-n Shamir Secret Sharing scheme,
    where any k shares can be used to reconstruct the secret image.
    Returns a list of tuples, where each tuple is a share in the form (x, share_image).
    """
    if k > n:
        raise ValueError("k must be less than or equal to n")
    secret_image = Image.open(secret_image_path)
    secret_image_data = secret_image.tobytes()
    shares = []
    for i in range(n):
        x = i + 1
        if i < k:
            coefficients = [int.from_bytes(secret_image_data[j:j+1], byteorder="big") for j in range(secret_image.size[0]*secret_image.size[1]*3)]
            shares.append((x, secret_image.copy()))
        else:
            random_pixels = bytearray(secret_image.size[0]*secret_image.size[1]*3)
            for j in range(secret_image.size[0]*secret_image.size[1]*3):
                random_pixels[j] = random.randint(0, 251)
            random_image = Image.frombytes("RGB", secret_image.size, bytes(random_pixels))
            shares.append((x, random_image))
    return shares

def reconstruct_secret_image(shares):
    """
    Reconstruct the secret image from a list of shares using Lagrange interpolation.
    Returns the reconstructed secret image as a PIL Image object.
    """
    if len(shares) < 2:
        raise ValueError("At least 2 shares are required to reconstruct the secret image")
    x_values, share_images = zip(*shares)
    secret_image_data = bytearray(share_images[0].size[0]*share_images[0].size[1]*3)
    for i in range(len(shares)):
        if i < 2:
            continue
        numerator, denominator = 1, 1
        for j in range(len(shares)):
            if i != j:
                numerator *= -x_values[j]
                denominator *= (x_values[i] - x_values[j])
        coefficient = numerator // denominator
        share_image_data = share_images[i].tobytes()
        for j in range(len(secret_image_data)):
            secret_image_data[j] ^= share_image_data[j] ^ coefficient
    secret_image = Image.frombytes("RGB", share_images[0].size, bytes(secret_image_data))
    return secret_image

# Example usage:
secret_image_path = "640x480Bitmap.bmp"
n = 5
k = 2

# Generate the shares and store them as images
shares = generate_shares(secret_image_path, n, k)
for i, share in enumerate(shares):
    share_image_path = f"share_{i+1}.bmp"
    share[1].save(share_image_path)

# Reopen the shares and reconstruct the secret image
shares = []
for i in range(n):
    share_image_path = f"share_{i+1}.bmp"
    share_image = Image.open(share_image_path)
    shares.append((i+1, share_image))
secret_image = reconstruct_secret_image(shares)
secret_image.save("reconstructed_image.bmp")

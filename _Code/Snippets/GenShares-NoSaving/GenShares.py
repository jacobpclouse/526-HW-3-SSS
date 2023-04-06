import random
from PIL import Image

def generate_shares(secret, n, k):
    """
    Generate n shares of the secret using a 2-out-of-n Shamir Secret Sharing scheme,
    where any k shares can be used to reconstruct the secret.
    Returns a list of tuples, where each tuple is a share in the form (x, y).
    """
    if k > n:
        raise ValueError("k must be less than or equal to n")
    coefficients = [secret] + [random.randint(1, 2**32-1) for _ in range(k-1)]
    shares = []
    for i in range(n):
        x = i + 1
        y = sum([coefficients[j] * x**j for j in range(k)])
        shares.append((x, y))
    return shares

def reconstruct_secret(shares):
    """
    Reconstruct the secret from a list of shares using Lagrange interpolation.
    Returns the reconstructed secret.
    """
    if len(shares) < 2:
        raise ValueError("At least 2 shares are required to reconstruct the secret")
    x_values, y_values = zip(*shares)
    secret = 0
    for i in range(len(shares)):
        numerator, denominator = 1, 1
        for j in range(len(shares)):
            if i != j:
                numerator *= -x_values[j]
                denominator *= (x_values[i] - x_values[j])
        secret += y_values[i] * numerator // denominator
    return secret

def encrypt_image(image_path, n, k):
    """
    Encrypt an image using Shamir Secret Sharing.
    Returns a list of n shares.
    """
    with open(image_path, "rb") as f:
        image_data = f.read()
    binary_data = "".join(format(byte, "08b") for byte in image_data)
    shares = generate_shares(int(binary_data, 2), n, k)
    return shares

def decrypt_image(shares):
    """
    Decrypt an image using Shamir Secret Sharing.
    Returns the decrypted image data as a bytes object.
    """
    secret = reconstruct_secret(shares)
    binary_data = bin(secret)[2:]
    padding = 8 - len(binary_data) % 8
    binary_data = "0" * padding + binary_data
    bytes_data = bytes(int(binary_data[i:i+8], 2) for i in range(0, len(binary_data), 8))
    return bytes_data

# Example usage:
# image_path = "example_image.png"
image_path = "640x480Bitmap.bmp"
n = 5
k = 2

# Encrypt the image
shares = encrypt_image(image_path, n, k)

# Decrypt the image
decrypted_data = decrypt_image(shares)

# Save the decrypted image to a file
with open("decrypted_image.bmp", "wb") as f:
    f.write(decrypted_data)

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

def share_to_image(share):
    """
    Convert a share to a grayscale image.
    Returns the image as a PIL Image object.
    """
    x, y = share
    x_binary = format(x, "08b")
    y_binary = format(y, "08b")
    pixel_data = [int(x_binary[i] + y_binary[i], 2) for i in range(8)]
    image = Image.new("L", (2, 1))
    image.putdata(pixel_data)
    return image

def image_to_share(image):
    """
    Convert a grayscale image to a share.
    Returns the share as a tuple (x, y).
    """
    pixel_data = list(image.getdata())
    x_binary = "".join(format(pixel_data[i], "08b")[0] for i in range(8))
    y_binary = "".join(format(pixel_data[i], "08b")[1] for i in range(8))
    x = int(x_binary, 2)
    y = int(y_binary, 2)
    return (x, y)

def encrypt_image(image_path, n, k):
    """
    Encrypt an image using Shamir Secret Sharing.
    Returns a list of n shares, where each share is a grayscale image.
    """
    with open(image_path, "rb") as f:
        image_data = f.read()
    binary_data = "".join(format(byte, "08b") for byte in image_data)
    shares = generate_shares(int(binary_data, 2), n, k)
    image_shares = [share_to_image(share) for share in shares]
    return image_shares

def decrypt_image(shares):
    """
    Decrypt an image encrypted with Shamir Secret Sharing.
    Returns the decrypted image as a PIL Image object.
    """
    shares_data = [image_to_share(image) for image in shares]
    secret = reconstruct_secret(shares_data)
    binary_data = format(secret, "b")
    # pad the binary data with zeros to make its length a multiple of 8
    padded_binary_data = binary_data.zfill((len(binary_data) + 7) // 8 * 8)
    byte_data = bytes(int(padded_binary_data[i:i+8], 2) for i in range(0, len(padded_binary_data), 8))
    image = Image.frombytes("L", (len(byte_data), 1), byte_data)
    return image

# --- 
image_path = "640x480Bitmap.bmp"
n = 5
k = 3
image_shares = encrypt_image(image_path, n, k)
for i, image_share in enumerate(image_shares):
    image_share.save(f"image_share_{i}.bmp")
    recovered_shares = [Image.open(f"image_share_{i}.bmp") for i in range(k)]
    recovered_image = decrypt_image(recovered_shares)
    recovered_image.show()

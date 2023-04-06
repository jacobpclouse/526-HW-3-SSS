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
        if coefficient < 0 or coefficient > 255:
            raise ValueError(f"Invalid coefficient value: {coefficient}")
        share_image_data = share_images[i].tobytes()
        for j in range(len(secret_image_data)):
            secret_image_data[j] ^= share_image_data[j] ^ coefficient
            if secret_image_data[j] < 0 or secret_image_data[j] > 255:
                raise ValueError(f"Invalid secret image data value: {secret_image_data[j]}")
    secret_image = Image.frombytes("RGB", share_images[0].size, bytes(secret_image_data))
    return secret_image

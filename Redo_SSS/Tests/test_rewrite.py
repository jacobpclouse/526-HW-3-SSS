from PIL import Image
import numpy as np
from scipy.interpolate import lagrange as lag

n = 5
r = 3
path = "1.bmp"

def read_image(path):
    with Image.open(path).convert('L') as img:
        img_array = np.array(img)
    return img_array.flatten(), img_array.shape

def polynomial(img, n, r):
    num_pixels = img.shape[0]
    coef = np.random.randint(low=0, high=251, size=(num_pixels, r - 1))
    gen_imgs = []
    for i in range(1, n + 1):
        base = np.array([i ** j for j in range(1, r)])
        base = coef @ base
        img_ = (img + base) % 251
        gen_imgs.append(img_)
    return np.array(gen_imgs)

def lagrange(x, y, num_points, x_test):
    l = np.zeros(num_points)
    for k in range(num_points):
        l[k] = 1
        for k_ in range(num_points):
            if k != k_:
                l[k] = l[k] * (x_test - x[k_]) / (x[k] - x[k_])
    L = 0
    for i in range(num_points):
        L += y[i] * l[i]
    return L

def decode(imgs, index, r, n):
    assert imgs.shape[0] >= r
    x = np.array(index)
    dim = imgs.shape[1]
    img = []
    for i in range(dim):
        if (i + 1) % 10000 == 0:
            print(f"decoding {i+1}th pixel")
        y = imgs[:, i]
        poly = lag(x, y, r, 0)
        pixel = poly % 251
        img.append(pixel)
    return np.array(img)

if __name__ == "__main__":
    img_flattened, shape = read_image(path)
    gen_imgs = polynomial(img_flattened, n, r)
    to_save = gen_imgs.reshape(n, *shape)
    for i, img in enumerate(to_save):
        Image.fromarray(img.astype(np.uint8)).save(f"test2_{i+1}.jpeg")
    origin_img = decode(gen_imgs[0:r, :], list(range(1, r + 1)), r, n)
    origin_img = origin_img.reshape(*shape)
    Image.fromarray(origin_img.astype(np.uint8)).save("test2_origin.jpeg")

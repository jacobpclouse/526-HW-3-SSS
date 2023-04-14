from PIL import Image
import numpy as np
from scipy.interpolate import lagrange as lag


n = 5
r = 3
path = "1.bmp"

# feel pretty good about read image
def read_image(path):
    img = Image.open(path).convert('L') # converting to grayscale image when opening
    # img.show()
    img_array = np.asarray(img)
    # print(img_array.shape) # this is the dimensions that we are getting 
    
    return img_array.flatten(), img_array.shape
    # The flatten() method is used to convert a multidimensional array into a one-dimensional array or a vector.


def polynomial(img, n, r):
    num_pixels = img.shape[0] # this gets the total number of pixels in the image
    coef = np.random.randint(low = 0, high = 251, size = (num_pixels, r - 1)) # this creates an array of arrays that is length of the number of pixels, and each sub array is k-1 columns (etc if we need 3 shares to reconstruct, than each sub array has 2 values)
    # print(coef.shape)
    gen_imgs = []
    for i in range(1, n + 1):
        base = np.array([i ** j for j in range(1, r)])
        # print(base)
        base = np.matmul(coef, base)
        # print(base.shape)
        # print(img.shape)
        img_ = img + base
        img_ = img_ % 251
        gen_imgs.append(img_)

    return np.array(gen_imgs)

def lagrange(x, y, num_points, x_test):
    # 所有的基函数值，每个元素代表一个基函数的值
    l = np.zeros(shape=(num_points, ))

    # 计算第k个基函数的值
    for k in range(num_points):
        # 乘法时必须先有一个值
        # 由于l[k]肯定会被至少乘n次，所以可以取1
        l[k] = 1
        # 计算第k个基函数中第k_个项（每一项：分子除以分母）
        for k_ in range(num_points):
            # 这里没搞清楚，书中公式上没有对k=k_时，即分母为0进行说明
            # 有些资料上显示k是不等于k_的
            if k != k_:
                # 基函数需要通过连乘得到
                l[k] = l[k]*(x_test-x[k_])/(x[k]-x[k_])
            else:
                pass 
    # 计算当前需要预测的x_test对应的y_test值        
    L = 0
    for i in range(num_points):
        # 求所有基函数值的和
        L += y[i]*l[i]
    return L

def decode(imgs, index, r, n):
    assert imgs.shape[0] >= r
    # print(imgs.shape)
    x = np.array(index)
    dim = imgs.shape[1]
    img = []
    for i in range(dim):
        if (i + 1) % 10000 == 0:
            print("decoding {} th pixel".format(i + 1))
        y = imgs[:, i]
        poly = lag(x, y)
        pixel = poly(0) % 251
        # print(x)
        # print(y)
        # pixel = lagrange(x, y, r, 0) % 251
        img.append(pixel)
    return np.array(img)



    
if __name__ == "__main__":
    img_flattened, shape = read_image(path)
    gen_imgs = polynomial(img_flattened, n = n, r = r)
    to_save = gen_imgs.reshape(n, *shape)
    for i, img in enumerate(to_save):
        Image.fromarray(img.astype(np.uint8)).save("test2_{}.jpeg".format(i + 1))
    origin_img = decode(gen_imgs[0:r, :], list(range(1, r + 1)), r = r, n = n)
    origin_img = origin_img.reshape(*shape)
    Image.fromarray(origin_img.astype(np.uint8)).save("test2_origin.jpeg")



    
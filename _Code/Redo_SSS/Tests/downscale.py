#--- Downscale Image Method ---
def downscale_image(img, width, height):
    down_width = width // 2
    down_height = height // 2
    down_image = [[0 for _ in range(down_width)] for _ in range(down_height)]
    for i in range(0, height, 2):
        for j in range(0, width, 2):
            total = 0
            for m in range(2):
                for n in range(2):
                    total += img[i+m][j+n]
            down_image[i//2][j//2] = total // 4

    return down_image



#--- Generate Downscaled Shares ---
scaled_gen_imgs = []
for i in range(n):
    scaled_img = downscale_image(gen_imgs[i], orig_size[0], orig_size[1])
    scaled_gen_imgs.append(scaled_img)

#--- Randomly Pick Two Downscaled Shares --- CAN REMOVE THIS AND JUST PICK 1 and 2
pick = random.sample([0, 1, 2], 2)
is1 = scaled_gen_imgs[pick[0]]
is2 = scaled_gen_imgs[pick[1]]

#--- Reconstruct Downscaled Image ---
is_ = [[0 for _ in range(len(is1[0])2)] for _ in range(len(is1)2)]
for i in range(0, len(is1)):
    for j in range(0, len(is1[0])):
        is_[i2][j2] = is1[i][j]
        is_[i2+1][j2] = is1[i][j]
        is_[i2][j2+1] = is1[i][j]
        is_[i2+1][j2+1] = is2[i][j]


# --- Display Original and Reconstructed Downscaled Image ---
# img = Image.open(path)
# img.show(title="Original Image")
img_downscaled = Image.fromarray(np
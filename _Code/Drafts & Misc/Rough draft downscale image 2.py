from PIL import Image

def downscale_image(image_path):
    with Image.open(image_path) as img:
        width, height = img.size
        new_width = width // 2
        new_height = height // 2
        new_image = Image.new('RGB', (new_width, new_height))
        for x in range(new_width):
            for y in range(new_height):
                avg_r = (img.getpixel((2*x, 2*y))[0] + img.getpixel((2*x+1, 2*y))[0] + img.getpixel((2*x, 2*y+1))[0] + img.getpixel((2*x+1, 2*y+1))[0]) // 4
                avg_g = (img.getpixel((2*x, 2*y))[1] + img.getpixel((2*x+1, 2*y))[1] + img.getpixel((2*x, 2*y+1))[1] + img.getpixel((2*x+1, 2*y+1))[1]) // 4
                avg_b = (img.getpixel((2*x, 2*y))[2] + img.getpixel((2*x+1, 2*y))[2] + img.getpixel((2*x, 2*y+1))[2] + img.getpixel((2*x+1, 2*y+1))[2]) // 4
                new_image.putpixel((x, y), (avg_r, avg_g, avg_b))
        return new_image

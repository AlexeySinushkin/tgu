from PIL import Image, ImageDraw

source_img = Image.open("example.bmp").convert("RGBA")
width, height = source_img.size
draw = ImageDraw.Draw(source_img)
if height>1:
    most_right_index = width - 1
    for j in range(1, height-1, 2):
        draw.line(((0, j), (most_right_index, j)), fill="blue")
source_img.save("example_modified.bmp", "BMP")
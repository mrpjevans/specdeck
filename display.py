import os
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import ST7789 as ST7789

disp = None

def init():
    global disp
    disp = ST7789.ST7789(
        height=240,
        rotation=90,
        port=0,
        cs=ST7789.BG_SPI_CS_FRONT,  # BG_SPI_CS_BACK or BG_SPI_CS_FRONT
        dc=9,
        backlight=19,               # 18 for back BG slot, 19 for front BG slot.
        spi_speed_hz=80 * 1000 * 1000,
        offset_left=0,
        offset_top=0
    )
    disp.begin()

def display(image_file, title):
    global disp

    if not os.path.isfile(image_file):
        titleImage = Image.new("RGB", (240, 240))
        draw = ImageDraw.Draw(titleImage)
        font = ImageFont.truetype(os.path.dirname(os.path.realpath(__file__)) + "/zx_spectrum-7.ttf", 30)
        draw.text((0,100), title, font=font, fill=(255, 255, 255))
        disp.display(titleImage)
        return

    image = Image.open(image_file)

    if image.width > 240 or image.height > 240:
        if image.width > image.height:
            ratio = image.height / image.width
            newWidth = 240
            newHeight = round(240 * ratio)
        else:
            ratio = image.width / image.height
            newWidth = round(240 * ratio)
            newHeight = 240
        image = image.resize((newWidth, newHeight))

    newImage = Image.new(image.mode, (240, 240))
    left_offset = 120 - round(image.width /2 ) if image.width < 240 else 0
    newImage.paste(image, (left_offset, 0, image.width + left_offset, image.height))
    
    disp.display(newImage)

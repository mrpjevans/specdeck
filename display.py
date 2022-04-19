from PIL import Image
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

def display(image_file):
    global disp

    image = Image.open(image_file)

    if image.width > 240:
        ratio = image.height / image.width
        image = image.resize((240, round(240 / ratio)))

    newImage = Image.new(image.mode, (240, 240))
    left_offset = 120 - round(image.width /2 )
    newImage.paste(image, (left_offset, 0, image.width + left_offset, image.height))
    
    disp.display(newImage)

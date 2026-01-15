import board
import displayio

import terminalio
from adafruit_display_text import label
from i2cdisplaybus import I2CDisplayBus

import adafruit_displayio_ssd1306

import time

import board
import busio
from digitalio import DigitalInOut, Direction, Pull

from adafruit_pm25.i2c import PM25_I2C

displayio.release_displays()

oled_reset = board.D9

i2c = board.I2C()  # uses board.SCL and board.SDA
display_bus = I2CDisplayBus(i2c, device_address=0x3D, reset=oled_reset)
reset_pin = None
pm25 = PM25_I2C(i2c, reset_pin)

WIDTH = 128
HEIGHT = 64
#BORDER = 5

display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=WIDTH, height=HEIGHT)

# Make the display context
splash = displayio.Group()
display.root_group = splash

color_bitmap = displayio.Bitmap(WIDTH, HEIGHT, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x000000

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# Draw a smaller inner rectangle
#inner_bitmap = displayio.Bitmap(WIDTH - BORDER * 2, HEIGHT - BORDER * 2, 1)
#inner_palette = displayio.Palette(1)
#inner_palette[0] = 0x000000  # Black
#inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=BORDER, y=BORDER)
#splash.append(inner_sprite)

pm10_text_area = label.Label(terminalio.FONT, text="", color=0xFFFFFF, x=6, y=4)
splash.append(pm10_text_area)

pm25_text_area = label.Label(terminalio.FONT, text="", color=0xFFFFFF, x=6, y=20)
splash.append(pm25_text_area)

pm100_text_area = label.Label(terminalio.FONT, text="", color=0xFFFFFF, x=6, y=36)
splash.append(pm100_text_area)

while True:
    time.sleep(1)

    try:
        aqdata = pm25.read()
    except RuntimeError:
        print("Unable to read from sensor, retrying...")
        continue

    pm10_text_area.text = str.format("PM 1.0:  {}", aqdata["pm10 standard"])
    pm25_text_area.text = str.format("PM 2.5:  {}", aqdata["pm25 standard"])
    pm100_text_area.text = str.format("PM 10.0: {}", aqdata["pm100 standard"])

    print("---------------------------------------")
    print("Particles > 0.3um / 0.1L air:", aqdata["particles 03um"])
    print("Particles > 0.5um / 0.1L air:", aqdata["particles 05um"])
    print("Particles > 1.0um / 0.1L air:", aqdata["particles 10um"])
    print("Particles > 2.5um / 0.1L air:", aqdata["particles 25um"])
    print("Particles > 5.0um / 0.1L air:", aqdata["particles 50um"])
    print("Particles > 10 um / 0.1L air:", aqdata["particles 100um"])
    print("---------------------------------------")

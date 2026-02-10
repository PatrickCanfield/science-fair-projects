import board
import displayio

import terminalio
from adafruit_display_text import label
from i2cdisplaybus import I2CDisplayBus

import adafruit_displayio_ssd1306
import adafruit_ens160

import time

import board
import busio
from digitalio import DigitalInOut, Direction, Pull

from adafruit_pm25.i2c import PM25_I2C

displayio.release_displays()

oled_reset = board.D9

i2c = board.I2C()  # uses board.SCL and board.SDA

reset_pin = None
pm25 = PM25_I2C(i2c, reset_pin)
ens = adafruit_ens160.ENS160(i2c)

WIDTH = 128
HEIGHT = 64
#BORDER = 5
def aqiname(value):
    if (value == 1):
        return "Good"
    elif (value == 2):
        return "Moderate"
    elif (value == 3):
        return "Sensitive"
    elif (value == 4):
        return "Unhealthy"
    elif (value == 5):
        return "Very Unhealthy"
    elif (value == 0):
        return "Hazardous"
    else:
        return "Error"

display_bus = I2CDisplayBus(i2c, device_address=0x3D, reset=oled_reset)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=WIDTH, height=HEIGHT)

# Make the display context
screen = displayio.Group()
display.root_group = screen

color_bitmap = displayio.Bitmap(WIDTH, HEIGHT, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x000000

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
screen.append(bg_sprite)

header_text_area = label.Label(terminalio.FONT, text="-- Particulates --", color=0xFFFFFF, x=0, y=4)
screen.append(header_text_area)

pm10_text_area = label.Label(terminalio.FONT, text="", color=0xFFFFFF, x=0, y=20)
screen.append(pm10_text_area)

pm25_text_area = label.Label(terminalio.FONT, text="", color=0xFFFFFF, x=0, y=32)
screen.append(pm25_text_area)

pm100_text_area = label.Label(terminalio.FONT, text="", color=0xFFFFFF, x=0, y=44)
screen.append(pm100_text_area)

aqi_text_area = label.Label(terminalio.FONT, text="", color=0xFFFFFF, x=0, y=56)
screen.append(aqi_text_area)

while True:
    time.sleep(1)

    try:
        aqdata = pm25.read()
    except RuntimeError:
        print("Unable to read from sensor, retrying...")
        continue

    aqi_text_area.text = str.format("AQI: {}", aqiname(ens.AQI))
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

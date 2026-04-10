import board
import displayio

import terminalio
from adafruit_display_text import label
from i2cdisplaybus import I2CDisplayBus

import adafruit_displayio_ssd1306
import adafruit_ens160

import time
import adafruit_thermistor
thermistor = adafruit_thermistor.Thermistor(
    board.TEMPERATURE, 10000, 10000, 25, 3950)

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
def getaqi():
    if (aqdata["pm25 standard"] < 9 and aqdata["pm25 standard"]>-1):
        return "Good"
    elif (aqdata["pm25 standard"] < 35 and aqdata["pm25 standard"]>-1):
        return "Moderate"
    elif (aqdata["pm25 standard"] < 55 and aqdata["pm25 standard"]>-1):
        return "Sensitive"
    elif (aqdata["pm25 standard"] < 125 and aqdata["pm25 standard"]>-1):
        return "Unhealthy"
    elif (aqdata["pm25 standard"] < 225 and aqdata["pm25 standard"]>-1):
        return "Very Unhealthy"
    elif (aqdata["pm25 standard"] > 224 and aqdata["pm25 standard"]>-1):
        return "Hazardous"
    else:
        return "Error"


display_bus = I2CDisplayBus(i2c, device_address=0x3D, reset=oled_reset)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=WIDTH, height=HEIGHT)

# Make the display context
screen = displayio.Group()
display.root_group = screen

color_bitmap = displayio.Bitmap(WIDTH, HEIGHT, 1)
color_palette = displayio.Palette(2)
color_palette[0] = 0x000000
color_palette[1] = 0xFFFFFF

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
screen.append(bg_sprite)

header_text_area = label.Label(terminalio.FONT, text="  -- Particulates --", x=0, y=4)
screen.append(header_text_area)

pm10_text_area = label.Label(terminalio.FONT, text="", x=0, y=20)
screen.append(pm10_text_area)

pm25_text_area = label.Label(terminalio.FONT, text="", x=0, y=32)
screen.append(pm25_text_area)

pm100_text_area = label.Label(terminalio.FONT, text="", x=0, y=44)
screen.append(pm100_text_area)

aqi_text_area = label.Label(terminalio.FONT, text="", x=68, y=44)
screen.append(aqi_text_area)

voc_text_area = label.Label(terminalio.FONT, text="", x=68, y=20)
screen.append(voc_text_area)

co2_text_area = label.Label(terminalio.FONT, text="", x=68, y=32)
screen.append(co2_text_area)

temp_text_area = label.Label(terminalio.FONT, text="", x=0, y=56)
screen.append(temp_text_area)

degC_text_area = label.Label(terminalio.FONT, text="", x=68, y=56)
screen.append(degC_text_area)

for i in range(20,68,12):
    screen.append(label.Label(terminalio.FONT, text="|", x=64, y=i))

while True:
    time.sleep(1)

    try:
        aqdata = pm25.read()
    except RuntimeError:
        print("Unable to read from sensor, retrying...")
        continue

    aqi_text_area.text = str.format("~AQI:{}", getaqi())
    voc_text_area.text = str.format("VOC:{}", ens.TVOC)
    co2_text_area.text = str.format("CO2:{}", ens.eCO2)
    pm10_text_area.text = str.format("PM 1.0:{}", aqdata["pm10 standard"])
    pm25_text_area.text = str.format("PM 2.5:{}", aqdata["pm25 standard"])
    pm100_text_area.text = str.format("PM 10: {}", aqdata["pm100 standard"])
    temp_text_area.text = str.format("TEMP F:{}", round((thermistor.temperature*1.8)+32))
    degC_text_area.text = str.format("TEMP C:{}", round(thermistor.temperature))

    print("---------------------------------------")
    print("Particles > 0.3um / 0.1L air:", aqdata["particles 03um"])
    print("Particles > 0.5um / 0.1L air:", aqdata["particles 05um"])
    print("Particles > 1.0um / 0.1L air:", aqdata["particles 10um"])
    print("Particles > 2.5um / 0.1L air:", aqdata["particles 25um"])
    print("Particles > 5.0um / 0.1L air:", aqdata["particles 50um"])
    print("Particles > 10 um / 0.1L air:", aqdata["particles 100um"])
    print("---------------------------------------")

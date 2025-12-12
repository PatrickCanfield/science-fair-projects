import board
import digitalio
import neopixel

# MiniCPX written by Patrick's dad to free 4 kb of RAM,
# so Patrick could focus on the science rather than Out of Memory errors.
class MiniCPX:
	def __init__(self):
		# LEDs
		self._led = digitalio.DigitalInOut(board.D13)
		self._led.switch_to_output()
		self._pixels = neopixel.NeoPixel(board.NEOPIXEL,10)
		
		# Buttons
		self._a = digitalio.DigitalInOut(board.BUTTON_A)
		self._a.switch_to_input(pull=digitalio.Pull.DOWN)
		self._b = digitalio.DigitalInOut(board.BUTTON_B)
		self._b.switch_to_input(pull=digitalio.Pull.DOWN)

	@property
	def red_led(self) -> bool:
		return self._led.value

	@red_led.setter
	def red_led(self, value: bool) -> None:
		self._led.value = value

	@property
	def pixels(self) -> neopixel.NeoPixel:
		return self._pixels

	@property
	def button_a(self) -> bool:
		return self._a.value

	@property
	def button_b(self) -> bool:
		return self._b.value
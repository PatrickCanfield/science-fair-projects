#May20 build55
import pulseio
import board
import adafruit_irremote
import gc
import time

from MiniCpx import MiniCPX

print("Memory at 10:", gc.mem_free())

# MiniCPX written by Patrick's dad to free 4 kb of RAM,
# so Patrick could focus on the science rather than Out of Memory errors.
cpx = MiniCPX()

print("Memory at 15:", gc.mem_free())

# Creation of the encoder is largely from
# Adafruit Circuit Playground Express IR tutorial
# https://learn.adafruit.com/infrared-ir-receive-transmit-circuit-playground-express-circuit-python/overview

# Listens for infrared signals using the IR receiver.
pulsein = pulseio.PulseIn(board.IR_RX, maxlen=200, idle_state=True)
# Decodes IR pulses and turns them into numbers.
decoder = adafruit_irremote.GenericDecode()
# Used to send infrared signals on the IR transmitter @ 38KHz.
pulseout = pulseio.PulseOut(board.IR_TX, frequency=38000, duty_cycle=2 ** 15)
# Encodes pulseout and a tuple of numbers into IR pulses.
encoder = adafruit_irremote.GenericTransmit(header=[9000, 4500],
                                            one=[560, 1700],
                                            zero=[560, 560],
                                            trail=0)

print("Memory at 31:", gc.mem_free())

def blink(rgb):
    for i in range(10):
        cpx.pixels[i] = (rgb[0],rgb[1],rgb[2])
    time.sleep(0.8)
    cpx.pixels.fill(0)
    time.sleep(0.4)
    gc.collect()

name = "Micheal"

def printreceive(x):
    print("<"+name+"> "+"I heard: "+x)

def printsend(x):
    print("<"+name+">"+"I'm sending: "+x)

MODE_WAIT = 0
MODE_SEND = 1
MODE_RECEIVE = 2
MODE_EXIT = 3
mode = MODE_WAIT

send_code = 0
send_count = 0
message = ""
msg_color = (0,0,0)

cpx.red_led = True
# Check for button press to begin communicating.
while mode == MODE_WAIT:
    if cpx.button_a:
        mode = MODE_SEND
        print("I want to send a message to someone in three seconds.")
        time.sleep(3)
        send_code = [224, 224, 208, 47]
        msg_color = (0,0,255)
        message = "Hello"
        cpx.red_led = False
    elif cpx.button_b:
        mode = MODE_RECEIVE
        name = "John"
        print("I'm listening for a message.")


while mode != MODE_EXIT:
    gc.collect()

    if mode == MODE_RECEIVE:
        cpx.led_red = True

        try:
            pulsein.resume()
            pulses = decoder.read_pulses(pulsein)
            gc.collect()

            received_code = decoder.decode_bits(pulses)

            pulsein.clear()
            pulses.clear()
            del pulses
            gc.collect()

            # hello
            if received_code == (224, 224, 208, 23) or received_code == (224, 224, 208, 47):
                printreceive("Hello.")
                blink((0,0,255))
                message = "What's up?"
                send_code = (255,2,255,0)
                msg_color = (255,71,147)
                mode = MODE_SEND
            # What's up
            elif received_code == (255, 2, 255, 0):
                printreceive("What's up?")
                blink((255,71,147))
                message = "Nothing much."
                send_code = (224,2,127,128)
                msg_color = (178,0,255)
                mode = MODE_SEND
            # Nothing much
            elif received_code == (224, 2, 127, 128) or received_code == (224, 2, 127, 64):
                printreceive("Nothing much.")
                blink((178,0,255))
                message = "I should leave."
                send_code = (224,2,191,64)
                msg_color = (0,255,255)
                mode = MODE_SEND
            # Same here
            elif received_code == (224, 2, 191, 64) or received_code == (224, 2, 191, 32):
                printreceive("I should leave.")
                blink((0,255,255))
                message = "Bye!"
                send_code = (224,128,128,27)
                msg_color = (182,227,0)
                mode = MODE_SEND
            # I should leave
            elif received_code == (224, 128, 128, 27) or received_code == (224, 128, 128, 13):
                printreceive("Bye!")
                blink((0,255,0))
                mode = MODE_EXIT
            # Me too
            # Ignore IR interference (e.g. TV Remote signals.)
            else:
                print("(▪▪▪I don't understand what", received_code, "means!!▪▪▪)")
        except Exception as e:
            pass
    elif mode == MODE_SEND:
        cpx.red_led = False

        printsend(message)
        blink(msg_color)
        encoder.transmit(pulseout, send_code)
        if send_code == (224,128,128,27):
            mode = MODE_EXIT
        else:
            print("I'm done speaking. Time to listen.")
            mode = MODE_RECEIVE
            time.sleep(1)
            pulsein.clear()

#blink((255,255,255))
#blink((255,106,0))
#blink((255,216,0))
#blink((0,255,0))
#blink((255,0,0))
#blink((178,0,255))

cpx.pixels[0]=(255,0,0)
cpx.pixels[1]=(255,200,0)
cpx.pixels[2]=(228,255,0)
cpx.pixels[3]=(0,255,0)
cpx.pixels[4]=(0,255,198)
cpx.pixels[5]=(0,255,255)
cpx.pixels[6]=(0,28,255)
cpx.pixels[7]=(128,0,255)
cpx.pixels[8]=(255,0,218)
cpx.pixels[9]=(255,0,34)
print("*CONVERSATION OVER*")
print("\"Thank you for checking out my project!\" -Patrick")
time.sleep(30)

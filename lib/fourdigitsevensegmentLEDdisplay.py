"""
# use this code in a separate file (code.py) to test this module

import board
import digitalio
import time
import fourdigitsevensegmentLEDdisplay as led_display

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

display_numbers = [9, 1.234, 150.667, 0.1, 9999, 0.123, 37.5, 0.123456, 1234.5678, 10, 37.5566]

while True:
    led.value = True

    for value in display_numbers:

        t_end = time.time() + 2
        while time.time() < t_end:
            led_display.display_number(value)

"""

import board
import digitalio
import time
import math

def clear_display():
    for bit in bits:
        bit.value = True

def clear_segments():
    for segment in segments:
        segment.value = False

def create_segments(pins):
    segments = []
    for pin in pins:
        led = digitalio.DigitalInOut(pin)
        led.direction = digitalio.Direction.OUTPUT
        segments.append(led)

    return segments


def create_bits(digits):
    bits = []
    for digit in digits:
        bit = digitalio.DigitalInOut(digit)
        bit.direction = digitalio.Direction.OUTPUT
        bits.append(bit)

    return bits

def display_number(number):
    dp = False #  variable to manage decimal point handling
    disp_digits = parse_number(number)
    #  we need a separate counter to skip the change in digit when encountering a decimal place
    n = 0
    #  have to use reversed() in conjunction with the order of the bits if you want the number to right-justify on the display
    for unit in reversed(disp_digits):
        bits[n].value = False

        if unit == '.':
            dp = True
            continue

        seg_map = numbers[unit]

        for m, segment in enumerate(seg_map):
            if segment == 1:
                segments[m].value = True
            elif dp is True:        # modify seg_map if last parse was a dp
                segments[7].value = True
                dp = False

        time.sleep(0.001)
        clear_display()
        clear_segments()
        n += 1


def parse_number(number):

    #  if number above or below - error
    if number > 9999 or number < 0.001:
        return 'Erro'
        #  raise Exception("Number must be between 9999 and 0.001")

    #  if it's more than 999 floor
    if number > 999:
        return str(math.floor(number))

    #  if it's greater than 10 and (implicitly) <= 999, check for decimal point and reduce to one or two dp if it's there
    if number >= 10:
        if number % 1:
            #  format to 1 or 2dp and return
            return '{0:.4g}'.format(number)
        else:
            return str(number)

    #  Otherwise the number will be < 10 check for decimal point and reduce to 3 dp if there is one
    if number % 1:
        #  format to  3dp and return
        return '{0:.3g}'.format(number)
    else:
        return str(number)

pins = [ #  pin - lcd pin
    board.GP20, #  2
    board.GP21, #  1
    board.GP10, #  11
    board.GP11, #  10
    board.GP12, #  7
    board.GP17, #  5
    board.GP18, #  4
    board.GP19  #  DP
]

digits = [ #  pin - lcd pin
    board.GP16, #  pin 6  (digit 4)
    board.GP13, #  pin 8  (digit 3)
    board.GP14, #  pin 9  (digit 2)
    board.GP15  #  pin 12 (digit 1)
]

numbers = {
    '0': [1, 1, 1, 1, 1, 0, 1, 0],
    '1': [0, 0, 0, 0, 1, 0, 1, 0],
    '2': [1, 1, 1, 0, 1, 1, 0, 0],
    '3': [1, 0, 1, 0, 1, 1, 1, 0],
    '4': [0, 0, 0, 1, 1, 1, 1, 0],
    '5': [1, 0, 1, 1, 0, 1, 1, 0],
    '6': [1, 1, 1, 1, 0, 1, 1, 0],
    '7': [0, 0, 1, 0, 1, 0, 1, 0],
    '8': [1, 1, 1, 1, 1, 1, 1, 0],
    '9': [1, 0, 1, 1, 1, 1, 1, 0],
    'E': [1, 1, 1, 1, 0, 1, 0, 0],
    'r': [0, 1, 0, 0, 0, 1, 0, 0],
    'o': [1, 1, 0, 0, 0, 1, 1, 0]
}

segments = create_segments(pins)
bits = create_bits(digits)



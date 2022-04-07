import board
import digitalio
import time
import math

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
        for segment in segments:
            segment.value = False

        if unit == '.':
            dp = True
            continue
            
        seg_map = numbers[unit]
        
        # modify seg_map if last parse was a dp
        if dp is True:
            seg_map[-1] = 1
            dp = False
        
        for m, segment in enumerate(seg_map):
            if segment == 1:
                segments[m].value = True
            
        time.sleep(0.001)
        bits[n].value = True
        n += 1
    

def parse_number(number):
    
    # if number above or below - error
    if number > 9999 or number < 0.001:
        return 'Erro'
        #  raise Exception("Number must be between 9999 and 0.001")

    # if it's more than 999 floor
    elif number > 999:
        return str(math.floor(number))

    # if it's between 10 and 999, check for decimal point and reduce to one or two dp if it's there
    elif number >= 10 and number <= 999:
        if number % 1 > 0:
            #  format to  1dp and return
            return '{0:.4g}'.format(number)
        else:
            return str(number)
    
    # if it's less than 10, check for decimal point and reduce to 3 dp if there is one
    elif number < 10:
        if number % 1 > 0:
            #  format to  3dp and return
            return '{0:.3g}'.format(number)
        else:
            return str(number)
            
    else:
        return 'Erro'

pins = [
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

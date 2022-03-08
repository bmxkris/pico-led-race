# Write your code here :

import board
import neopixel
import digitalio
from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.sparkle import Sparkle
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.sequence import AnimationSequence
from adafruit_led_animation.group import AnimationGroup
from adafruit_led_animation.color import RED, GREEN, BLUE, WHITE, YELLOW, PURPLE, AMBER
from adafruit_debouncer import Debouncer


num_pixels = 90
play_to = 90  # or num_pixels
brightness = 1

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT


def winner_animation(pixels, pixels2, button1, button2, reset_button):
    print("winning annimation")
    animations = AnimationSequence(
        Blink(pixels, speed=0.07, color=WHITE), 
        Comet(pixels, speed=0.0082 ,color=PURPLE, tail_length=10, bounce=True),
        Rainbow(pixels, speed=0.01, period=1.5),
        Rainbow(pixels, speed=0.01, period=1.5),
        Rainbow(pixels, speed=0.01, period=1.5),
        advance_interval=1.5,
        auto_clear=True,
    )
    
    while animations.cycle_count < 1 :
        animations.animate()
        
    standby_animation(pixels, pixels2, button1, button2, reset_button)


def create_button(gpio_pin):
    pin = digitalio.DigitalInOut(gpio_pin)
    pin.direction = digitalio.Direction.INPUT
    pin.pull = digitalio.Pull.DOWN
    return Debouncer(pin)

def increment_pixels(pixels, player):
        pixels[player] = GREEN
        pixels.show()
        player += 1
        return player

def init_game(pixels, pixels2, button1, button2, reset_button):
    animations = AnimationSequence(
        AnimationGroup(
            Pulse(pixels, speed=0.01, color=RED, period=1.5),
            Pulse(pixels2, speed=0.01, color=RED, period=1.5),
            sync=True,
        ),
        AnimationGroup(
            Pulse(pixels, speed=0.01, color=YELLOW, period=1.5),
            Pulse(pixels2, speed=0.01, color=YELLOW, period=1.5),
            sync=True,
        ),
        AnimationGroup(
            Pulse(pixels, speed=0.01, color=GREEN, period=1.5),
            Pulse(pixels2, speed=0.01, color=GREEN, period=1.5),
            sync=True,
        ),
        advance_interval=1.5,
        auto_clear=True,
    )
    
    while animations.cycle_count < 1:
        animations.animate()
    
    pixels.fill(RED)
    pixels2.fill(BLUE)
    pixels.show()
    pixels2.show()
    
    global play_to
    player1 = 0
    player2 = 0

    while True:
        led.value = True
        button1.update()
        button2.update()

        if button1.fell:
            print("Just pressed 1")
            print(player1)
            player1 = increment_pixels(pixels,player1)

        if button2.fell:
            print("Just pressed 2")
            print(player2)
            player2 = increment_pixels(pixels2,player2)

        if player1 == play_to:
            # animate
            print("Player 1 wins")
            winner_animation(pixels, pixels2, button1, button2, reset_button)

        elif player2 == play_to:
            print("Player 2 wins")
            winner_animation(pixels2, pixels, button1, button2, reset_button)

def standby_animation(pixels, pixels2, button1, button2, reset_button): 
    sparkle = AnimationGroup(
        Sparkle(pixels, speed=0.1, color=AMBER, num_sparkles=10),
        Sparkle(pixels2, speed=0.1, color=AMBER, num_sparkles=10),
    )
    
    while True:
        reset_button.update()
        #standby animation
        sparkle.animate()
        
        if reset_button.fell:
            print("Just pressed reset")
            init_game(pixels, pixels2, button1, button2, reset_button)


pixels = neopixel.NeoPixel(board.GP2, num_pixels, brightness=brightness, auto_write=False)
pixels2 = neopixel.NeoPixel(board.GP3, num_pixels, brightness=brightness, auto_write=False)

reset_button = create_button(board.GP14)
button1      = create_button(board.GP16)
button2      = create_button(board.GP17)

standby_animation(pixels, pixels2, button1, button2, reset_button)

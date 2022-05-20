# pico-led-race

Code to run a game on the Raspberry Pi Pico RP2040. The game has two buttons that players repeatidly press to increase the number of illuminated LEDs in an addressable LED strip. First to the end wins!

There is a third button that is used to start each game. The game can be powered by either connecting a 5V USB power supply or connecting 5V to either power rail.

There are two wiring diagram includes a 4-digit 7-segement display. The code will still run if you don't wire up the LCD display, so you can still run this game without the complexity of wiring the display. The display shows how long the winner took to reach the end. The code for the LCD display is specific to the wiring set up in this wiring diagram:

![Circuit diagram for pico-led-race](pico-led-race-circuit-diagram.png?raw=true "Circuit diagram for pico-led-race")

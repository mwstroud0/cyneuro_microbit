# Imports go at the top
from microbit import *
import radio

radio.config(group=42)
radio.on()

# Code in a 'while True:' loop repeats forever
while True:
    if(button_a.is_pressed() and button_b.is_pressed()):
        radio.send('straight') 
    elif(button_a.is_pressed() and not button_b.is_pressed()):
        radio.send('left')
    elif(not button_a.is_pressed() and button_b.is_pressed()):
        radio.send('right')
    elif(not button_a.is_pressed() and not button_b.is_pressed()):
        radio.send('stop')
    
    display.show(Image.HEART)

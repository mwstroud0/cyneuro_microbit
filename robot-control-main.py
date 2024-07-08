# Imports go at the top
from microbit import *
from Cutebot import *
import radio 
    
bot = CUTEBOT()
radio.config(group=42)
radio.on()
# Code in a 'while True:' loop repeats forever
while True:
    display.show(Image.SQUARE)
    
    message = radio.receive()
        
    if(message == 'straight'):
        bot.set_motors_speed(50,50)
    elif(message == 'left'):
        bot.set_motors_speed(0,25)
    elif(message == 'right'):
        bot.set_motors_speed(25,0)
    elif(message == 'stop'):
        bot.set_motors_speed(0,0)
    



sleep(1000)
    
display.scroll('Hello')

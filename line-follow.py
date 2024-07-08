# Imports go at the top
from microbit import *
from Cutebot import *

dis = CUTEBOT()

# Code in a 'while True:' loop repeats forever
max_speed = 40
straight_speed_split =  int(max_speed / 2)
turn_ratio = 0.8
strong_speed = int(max_speed * turn_ratio)
weak_speed = int(max_speed * (1-turn_ratio))

while True:
    i = dis.get_tracking()
    if i == 10:
        dis.set_motors_speed(weak_speed, strong_speed)
    if i == 1:
        dis.set_motors_speed(strong_speed, weak_speed)   
    if i == 11:
        dis.set_motors_speed(straight_speed_split, straight_speed_split) 
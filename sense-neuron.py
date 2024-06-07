# Imports go at the top
from microbit import *
import music

C=1                   #capacitance        
Vth = 1               #threshold voltage 
Vreset = 0            #reset voltage  
V=0;             #initial voltage
injection_factor = 0.015
feedback_factor = 1.015 #voltage runaway factor
decay_factor = 0.005

#adaptation_factor = 0.00001


# First scale the voltage to be between 0 and 9
def cap(val):
    if val > 9:
        return 9
    else:
        return val

# Code in a 'while True:' loop repeats forever
while True:
    if button_b.was_pressed():
        injection_factor = injection_factor + 0.002

    if button_a.was_pressed():
        injection_factor = injection_factor - 0.002

    if(injection_factor <= decay_factor):
        injection_factor = decay_factor + 0.001

    if pin_logo.is_touched():
        I = injection_factor
    else:
        I = 0

    # modified IF neuron
    V = feedback_factor * V + (I/C) - decay_factor 
    
    if V > Vth:
        music.pitch(200)
        sleep(20)
        music.stop()
        V = Vreset
    elif V <= 0:
        V = Vreset

    # Craft the image based on the voltage (0 - 1)
    ''' Using this pattern as a general structure
    display.show(Image('00300:'
                       '03630:'
                       '36963:'
                       '03630:'
                       '00300'))
    '''
  
    V_disp = round(V * 9)
    
    row1 = str(cap(V_disp)) + str(cap(V_disp)) + str(cap(V_disp*3)) + str(cap(V_disp)) + str(cap(V_disp)) + ":"
    row2 = str(cap(V_disp))+str(cap(V_disp*3))+str(cap(V_disp*6))+str(cap(V_disp*3))+str(cap(V_disp)) + ":"
    row3 = str(cap(V_disp*3))+str(cap(V_disp*6))+str(cap(V_disp*9))+str(cap(V_disp*6))+str(cap(V_disp*3)) + ":"
    row4 = str(cap(V_disp))+str(cap(V_disp*3))+str(cap(V_disp*6))+str(cap(V_disp*3))+str(cap(V_disp)) + ":"
    row5 = str(cap(V_disp))+str(cap(V_disp))+str(cap(V_disp*3))+str(cap(V_disp))+str(cap(V_disp))

    display.show(Image(row1+row2+row3+row4+row5))

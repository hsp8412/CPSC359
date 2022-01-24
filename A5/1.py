#Name: Sipeng He
#UCID: 30113342
#Feature:
#(1)Send the square wave, the duration of which is 100us, to the Pin 13.
#(2)Read the duration and the frequency of the square wave from Pin 11.

import time
import rp2
from machine import Pin, Timer

@rp2.asm_pio( set_init=rp2.PIO.OUT_LOW )
def square():
    label( "again" )
    set(pins, 1)   
    set(pins, 0) [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [22]
    jmp( "again" )

sm = rp2.StateMachine(0, square, freq=10000, set_base=Pin(13))
readPin = Pin(11, Pin.IN)

counter = 0
duration = []

sm.active(1)

def measure(timer):
    global duration, counter
    pulseDuration = sum(duration)/counter
    print("Frequency: {} Hz".format(counter))               
    print("Duration: {:.2f} us".format(pulseDuration))   #suppose to be 100us
    duration = []
    counter = 0

timer = Timer(period = 1000, mode = Timer.PERIODIC, callback = measure)

while True:
    t1 = time.ticks_us()
    
    while readPin.value() == 1 :
        pass
    
    t2 = time.ticks_us()
    
    duration.append(time.ticks_diff( t2, t1 ))
    counter = counter + 1
    
    while readPin.value() == 0 :
        pass




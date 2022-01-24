#Name: Sipeng He
#UCID: 30113342
#Feature:
#(1)Send the square wave, the duration of which is 100us, to Pin 13 to initiate the US-100 measurement.
#(2)Measure the distance by reading the pulse duration of the echo wave from Pin 12.
#(3)Print the distance measurement once every second.

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
readPin = Pin(12, Pin.IN)

duration = 0

sm.active(1)

def measure(timer):
    global duration, counter
    distance = 0.5 * duration * 343.0 * 1e-6
    print( "distance: {:10.2f}m".format( distance ) )

timer = Timer(period = 1000, mode = Timer.PERIODIC, callback = measure)

while True:
    t1 = time.ticks_us()
    
    while readPin.value() == 1 :
        pass
    
    t2 = time.ticks_us()
    
    duration = time.ticks_diff( t2, t1 )
    
    while readPin.value() == 0 :
        pass





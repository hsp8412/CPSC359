#Name: Sipeng He
#UCID: 30113342
#Feature:
#(1)Send the square wave, the duration of which is 100us, to Pin 13 to initiate the US-100 measurement.
#(2)Measure the distance by reading the pulse duration of the echo wave from Pin 12.
#(3)Print the distance measurement once every second.
#(4)Interrupt handlers are used to make the measurement of the echo wave and display the measured distance.


from machine import Pin, Timer
import rp2
import utime

tLast = utime.ticks_us()
measureCount = 0
duration = 0

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

def measure(pin):
    global tLast, measureCount, counter, duration
    t1 = utime.ticks_us()
    measureCount = measureCount + 1
    if measureCount%2 == 0:
        duration = utime.ticks_diff( t1, tLast )
    else:
        tLast = t1

def printResult(timer):
    global duration, counter
    distance = 0.5 * duration * 343.0 * 1e-6
    print( "distance: {:10.2f}m".format( distance ) )

triggerPin = 13
echoPin = 12

trigger = Pin( triggerPin, Pin.OUT )
echo = Pin( echoPin, Pin.IN )

trigger.off()

sm = rp2.StateMachine(0, square, freq=10000, set_base=Pin(triggerPin))
sm.active(1)

echo.irq(handler = measure, trigger = Pin.IRQ_RISING|Pin.IRQ_FALLING)
timer = Timer(period = 1000, mode = Timer.PERIODIC, callback = printResult)
        



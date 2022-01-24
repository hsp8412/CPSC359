# SNES module

# Name: Sipeng He
# UCID: 30113342
# Feature: implement an SNES class that can be used to:
# read if the buttons are pressed, and return the button list
# reset the pins when the game is terminated
# Date: 2021.11.23

import gpio
import time

CLK = 11
LAT = 9
DAT = 10

GPSET0 = 7
GPCLR0 = 10
GPLEV0 = 13

class SNES:
    buttonList = [ 'B', 'Y', 'Select', 'Start',
                   'Up', 'Down', 'Left', 'Right',
                   'A', 'X', 'L', 'R' ]
    
    # set the function of a given pin to be output
    # parameters:
    # g: an instance of the GPIO class
    # pin_num: the number of pin to be set
    def setOutput(self, g, pin_num):
        r = g.peek_reg(pin_num/10)
        r &= ~(7 << (3*(pin_num%10)))
        r |= (1 << (3*(pin_num%10)))
        g.poke_reg(r, pin_num/10)
    
    # set the function of a given pin to be input
    # parameters:
    # g: an instance of the GPIO class
    # pin_num: the number of pin to be set
    def setInput(self, g, pin_num):
        r = g.peek_reg(pin_num/10)
        r &= ~(7 << (3*(pin_num%10)))
        g.poke_reg(r, pin_num/10)
    
    # set a given pin to be high
    # parameters:
    # g: an instance of the GPIO class
    # pin_num: the number of pin to be set
    def GPSET(self, g, pin_num):
         r = 1 << pin_num
         g.poke_reg(r, GPSET0)
   
    # set a given pin to be low
    # parameters:
    # g: an instance of the GPIO class
    # pin_num: the number of pin to be set
    def GPCLR(self, g, pin_num):
        r = 1 << pin_num
        g.poke_reg(r, GPCLR0)
    
    # read the bit of data from the Data pin(10)
    # parameter:
    # g: an instance of the GPIO class
    def readDAT(self, g):
        r = g.peek_reg(GPLEV0)
        r >>= DAT
        r &= 1
        return r
    
    # read the SNES buttons, return the list of buttons pressed
    def read(self):
        snesWord = 0
        g = gpio.GPIO()
        
        self.setOutput(g, CLK)
        self.setOutput(g, LAT)
        self.setInput(g, DAT)
        
        self.GPSET(g, CLK)
        self.GPSET(g, LAT)
        time.sleep(12e-6)
        self.GPCLR(g, LAT)
        
        bitMask = 1
        while bitMask < 0x10000:
            time.sleep(6e-6)
            self.GPCLR(g, CLK)
            time.sleep(6e-6)
            bit = self.readDAT(g)
            if(bit):
                snesWord |= bitMask
            self.GPSET(g, CLK)
            bitMask <<= 1
            
        buttons = []
        for i, button in enumerate( SNES.buttonList ) :
            if not (snesWord & (1 << i)) :
                buttons.append( button )
        return buttons
    
    # reset the CLK, LAT pins to be low, and then set them to be output
    def clear(self):
        g = gpio.GPIO()
        self.GPCLR(g, CLK)
        self.GPCLR(g, LAT)
        self.setInput(g, CLK)
        self.setInput(g, LAT)
        
        
        
        



#Name: Sipeng He
#UCID: 30113342
#Class: GPIO
#Feature: a Cython wrapper class for the peek and poke method.
#Date: 2021.11.23

cdef extern from "gpio_c.c":
    int peek(int offset)
    void poke(long value, int offset)


class GPIO:
    #Function: peek_reg
    #Feature: return a 32-bit piece of data from the specified register
    #Input: offset: the offset of a register
    def peek_reg(self, int offset):
        return peek(offset)
    
    #Function: poke_reg
    #Feature: write a 32-bit piece of data into the specified register
    #Input: value: the data to be written into the register
    #offset: the offset of a register
    def poke_reg(self, int value, int offset):
        poke(value, offset)
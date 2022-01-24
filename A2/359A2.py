# 359A2.py - build ROM program for CPSC 359 Assignment 2

#
#
#   inputs: y2 y1 y0 x2 x1 x0
#   outputs:  Y2 Y1 Y0  0 l0 r00 r01  0 l1 r10 r11  0 l2 r20 r21 a00 a01 a10 a11  - note extra 0 added for alignment purpose
#
#   table0 has the otherwise/default cases
#
#           address(inputs)     data(outputs)
#       -------------------------------------------
table0 = [  [   "000xxx",          "0000100010001000000"    ],      #idle state
            [   "001xxx",          "0100000010101010000"    ],      #initialization
            [   "010xxx",          "0110111000000000000"    ],      #update r0
            [   "011xxx",          "1000000011100000000"    ],      #update r1
            [   "100xxx",          "0100000000001100110"    ],      #update r2
            [   "101xxx",          "1100000011100000000"    ],      #update r1(halt)
            [   "110xxx",          "1110000000001100110"    ],      #update r2(halt)
            [   "111xxx",          "1110000000000000000"    ]       #halt state
        ]

#   table1 has special state transitions - triggered by input
#
#           address(inputs)     data(outputs)
#       -------------------------------------------
table1 = [  [   "000001",           "0010100010001000000"    ],      #algorithm starts when start pin = 1(other pins = 0)
            [   "001x1x",           "1110000010101010000"    ],      #halt pin = 1 at state 001
            [   "010x1x",           "1010111000000000000"    ],      #halt pin = 1 at state 010
            [   "011x1x",           "1100000011100000000"    ],      #halt pin = 1 at state 011
            [   "100x1x",           "1110000000001100110"    ],      #halt pin = 1 at state 100
            [   "1111xx",           "0000000000000000000"    ]       #reset pin = 1 at halt state, resume idle state
        ]


#
# match string as binary number allowing for 'x' == don't care
#
def binaryMatch( val, s ) :
    valString = format(val, '06b' )
    for i in range(len(s) ) :
        if s[i] == 'x' : continue
        if s[i] != valString[i] : return False
    return True
    
# iterate through all ROM addresses in order 0-63
#    compare address to truth table element - if match, write data in ROM
# start with table0 - state stays the same default transitions
rom = 64 * [0]
for addr in range(64) :
    for entry in table0 :
        if binaryMatch( addr, entry[0] ) :
            rom[addr] = eval( '0b' + entry[1] )

# finish with table1 - state changes on input
for addr in range(64) :
    for entry in table1 :
        if binaryMatch( addr, entry[0] ) :
            rom[addr] = eval( '0b' + entry[1] )

# print out the rom as logisim likes it
for i in range( len(rom) ) :
    print( format( rom[i], '05x' ), end='' )
    if i % 16 == 15 :
        print()
    else :
        print( ' ', end='' )
        
    

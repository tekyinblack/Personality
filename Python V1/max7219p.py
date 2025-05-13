# max7219 16x16 driver for Personality robot
# This class is intended to send picture data to a max7219 controlled
# led matrix verbatim.
# the picture is coded as an array of 0's and 1's to make it human readable
# and is typically loaded from a file
# max7219 drivers typically send data for display as a column within the matrix
# so as to display characters and so clock data into the controller a colum at
# a time.
#
# this code based on previous work by Mike Causer 2017


from micropython import const
import framebuf

_NOOP = const(0)
_DIGIT0 = const(1)
_DECODEMODE = const(9)
_INTENSITY = const(10)
_SCANLIMIT = const(11)
_SHUTDOWN = const(12)
_DISPLAYTEST = const(15)

class Matrix16x16:
    def __init__(self, spi, cs, num):
        """
        Driver for cascading MAX7219 8x8 LED matrices.


        """
        self.spi = spi
        self.cs = cs
        self.cs.init(cs.OUT, True)
        self.buffer = bytearray(32)
        self.num = num

        self.init()

    def _write(self, command, data):
        self.cs(0)
        for m in range(self.num):
            self.spi.write(bytearray([command, data]))
        self.cs(1)

    def init(self):
        for command, data in (
            (_SHUTDOWN, 0),
            (_DISPLAYTEST, 0),
            (_SCANLIMIT, 7),
            (_DECODEMODE, 0),
            (_SHUTDOWN, 1),
        ):
            self._write(command, data)

# set brightnes level
    def brightness(self, value):
        if not 0 <= value <= 15:
            raise ValueError("Brightness out of range")
        self._write(_INTENSITY, value)
        

# clear the buffer by setting all to zero    
    def clear(self):
        for y in range(32):
            self.buffer[y] = 0

# clear the buffer by setting all to zero    
    def invert(self):
        for y in range(32):
            self.buffer[y] = ~(self.buffer[y])
  
# load an individual pixel into buffer  
    def loadpix(self,line,position,value):
        if (line >= 0 and line < 16 and position >= 0 and position <= 15):
            if line < 8:
                if position < 8:
                    offset = 2 + (line * 4)
                else:
                    offset = 3 + (line * 4)
                    position = position - 8
                
            else:
                line = line - 8
                if position < 8:
                    offset = (line * 4)
                else:
                    offset = 1 + (line * 4)
                    position = position - 8
            position = 7 - position

            if value != 0:
                self.buffer[offset] = self.buffer[offset] | 1 << position
            else:
                self.buffer[offset] = self.buffer[offset] & ~(1 << position)
            
        
# send buffer to array
    def show(self):
        for y in range(8):
            self.cs(0)
            for m in range(self.num):
                self.spi.write(bytearray([_DIGIT0 + y, self.buffer[(y * self.num) + m]]))
            self.cs(1)
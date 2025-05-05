# Add-on Robot Personality
The purpose of the code in this repository is to run a MAX7219 based matrix displays to provide a visual
output from a robot, or just for standalone fun, with output described in files.
The original version is based on Raspberry Pi Pico

An example of a test control file is shown below with a description of the simple syntax. The files can be 
used to show just a single image or setup to provide a degree of animation.

# Checkerboard
# Basic syntax of file
# At the beginning of a line a # sign, blank or anything not a reserved control is ignored
# '.' or 'X' means start of LED data '.' means OFF, 'X' is ON
# Lxxx moves left servo to position xxx 
# Ryyy moves right servo to position yyy
# Dxxx pauses file read for xxx tenths of a second
# AGAIN closes the file and reopens it, typically the last statement
# CLEAR clears the display of an image
#
# This example flashes a checkerboard display and waves the arms alternately
CLEAR
L180
R90
D10
#123456789ABCDEF
.X.X.X.X.X.X.X.X
X.X.X.X.X.X.X.X.
.X.X.X.X.X.X.X.X
X.X.X.X.X.X.X.X.
.X.X.X.X.X.X.X.X
X.X.X.X.X.X.X.X.
.X.X.X.X.X.X.X.X
X.X.X.X.X.X.X.X.
.X.X.X.X.X.X.X.X
X.X.X.X.X.X.X.X.
.X.X.X.X.X.X.X.X
X.X.X.X.X.X.X.X.
.X.X.X.X.X.X.X.X
X.X.X.X.X.X.X.X.
.X.X.X.X.X.X.X.X
X.X.X.X.X.X.X.X.
L90
R180
D10
X.X.X.X.X.X.X.X.
.X.X.X.X.X.X.X.X
X.X.X.X.X.X.X.X.
.X.X.X.X.X.X.X.X
X.X.X.X.X.X.X.X.
.X.X.X.X.X.X.X.X
X.X.X.X.X.X.X.X.
.X.X.X.X.X.X.X.X
X.X.X.X.X.X.X.X.
.X.X.X.X.X.X.X.X
X.X.X.X.X.X.X.X.
.X.X.X.X.X.X.X.X
X.X.X.X.X.X.X.X.
.X.X.X.X.X.X.X.X
X.X.X.X.X.X.X.X.
.X.X.X.X.X.X.X.X
AGAIN

# Personality Robot Addon Code for Instructables
# v1.0.1 updates from first public release
# added reset for servos
# correction to file handling

from machine import UART, Pin, SPI

# Import MicoPython max7219 library
import max7219p

# import Servo library
from servo import Servo

# Import time
import time

# initial file of display data
global display_data
display_data = "main.txt"

# AGAIN control variable
reload = False

# display update control
reshow = False

global delay_time
delay_time = 0

print("Starting...")

commands = UART(0, baudrate=115200, bits=8, tx=Pin(0), rx=Pin(1), timeout=100)

# initialise servo arms down
left_arm = Servo(21,1)
left_arm.ServoAngle(0)
right_arm = Servo(22,0)
right_arm.ServoAngle(0)

#Intialize the SPI
spi = SPI(0, baudrate=10000000, polarity=1, phase=0, sck=Pin(18), mosi=Pin(19))
ss = Pin(17, Pin.OUT)

# Create matrix display instant, which has four MAX7219 devices.
display = max7219p.Matrix16x16(spi, ss, 4)

#Set the display brightness. Value is 1 to 15.
display.brightness(5)

#Clear the display.
display.clear()
display.show()


# command processing
def command_proc(text):
    # signal indicates next actions
    # 0 is no action
    # 1 is AGAIN or FILE processing
    # 2 is QUIT
    signal = 0
    global display_data
    global delay_time
    print(text)
    
    # ignore defined comments
    if text[0:1] == '#':
        print ("Ignoring comment ",text)
        pass
    # process left servo position
    elif text[0:4] == 'LEFT':    # test for left servo position
        print ("Processing servo ", text)
        try:
            left_arm.ServoAngle(int(text[4:]))
        except:                                        
            pass
    # process right servo position    
    elif text[0:5] == 'RIGHT':    # test for right servo position
        print ("Processing servo ", text)
        try:
            right_arm.ServoAngle(int(text[5:]))
        except:                                        
            pass
    # delay
    elif text[0:5] == 'DELAY':    # test for delay
        print ("Processing delay ", text)
        try:
            delay_time = int(text[5:])/10                 
        except:
            pass
        print("Delay = ", delay_time)
    # check for repeat file processing
    elif text[0:5] == 'AGAIN':    # test for AGAIN
        print ("Scheduling file reload ", text)
        signal = 1

    # process display clear
    elif text[0:5] == "CLEAR":    # test for CLEAR
        print ("Clearing display ", text)
        display.clear()
        display.show()
        
    # process display inversion
    elif text[0:6] == "INVERT":    # test for INVERT
        print ("Inverting display ", text)
        display.invert()
        display.show()

    # exit processing
    elif text[0:4] == "QUIT":    # test for QUIT
        print ("End of processing  ", text)
        signal = 2
 
    # process new file name
    elif text[0:4] == "FILE":    # test for File processing
        print ("Loading new file ", text)
        try:           
            # get file name
            display_data = text[4:]
            print("New file = ", display_data)
        except:
            pass
        
    # assume display data
    else:
        if text[0:1] != '0':
            try:         # cast first character as hex into integer where not zero
                line_no = int(text[0:1],16)
            except:
                line_no = 99
        else:
            line_no = 0  # and where it is, set it to zero
        if line_no < 16:
            text = text[1:]
            print ("Processing line data ", line_no, text)
            for y in range(len(text)):
                if text[y] == 'X':
                    display.loadpix(line_no,y,1)
                elif text[y] == '.':
                    display.loadpix(line_no,y,0)
                
        # If line 15, display
        if line_no == 15:
            display.show()

    
    return signal


#try:
while True: # start of main program loop
    result = 0
    if commands.any() != 0:
        command = commands.readline().decode('utf-8').strip('\n\r')
        #print (command.strip('\n\r'))
        print(command)
        result = command_proc(command)
    if result == 2:
        break
    if delay_time != 0:
        time.sleep(delay_time)
        delay_time = 0
    while display_data != "": # loop while there is a file name to process
        try:      
            f = open(display_data)
        except:
            print ("Processing exception in filename ", display_data)
            display_data = ""
            break
        print ("Processing file ",display_data)
        if f:
            for x in f:
                result = command_proc(x)
                    # process file repeat <<< may move into elif statement later
                if result == 1:
                    break
                if delay_time != 0:
                    time.sleep(delay_time)
                    delay_time = 0
            # process AGAIN and FILE function by closing the file and not blanking the file name
            if result == 1:
                result = 0
                f.close
            else:
                f.close()
                display_data = ""
        if commands.any() != 0:
            break
     
#except:
#    pass

print("...Complete")

display.clear()
display.show()
left_arm.ServoAngle(0)
right_arm.ServoAngle(0)
print("Resetting servos")
time.sleep(1)
left_arm.deinit()
right_arm.deinit()
print("End")        



 
 
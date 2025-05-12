from servo import Servo
import time

servo1=Servo(21,1)
servo1.ServoAngle(0)
servo2=Servo(22,0)
servo2.ServoAngle(0)
time.sleep_ms(1000)


servo1.deinit()
servo2.deinit()
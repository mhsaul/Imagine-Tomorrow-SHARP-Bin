'''
@author Miles Saul
Date: May 24, 2015
Description: This program sorts a single item with the SHARP
sorting bin. The on the bin is first initialized, then after 
the user presses "Enter", the object is scanned and sorted
as trash or recycling
'''


from sort_functions import calculateIntensity, initServo, sortItem
import cv2
import RPIO
import time
from PIL import Image
from RPIO import PWM

#initialize servo
servo = PWM.Servo()
initServo(servo)

#wait for input
raw_input()
HIP = calculateIntensity() #calculate value of the highest intensity pixel
sortItem(HIP, servo) #sort the item
time.sleep(1) #allow the object to fall into the category
initServo(servo) #reinitialize the servo

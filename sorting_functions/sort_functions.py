"""
Created on Fri May 30 19:24:01 2014

@author: Miles Saul, Aneesh Pappu

This file is used to test if an object is recyclable.
It first scans in an image taken by a picamera. It then
grayscales the image and determines the highest intensity
pixel (HIP)_in the image. If the HIP is greater than the 
threshold of 40, the object is reflective and sorted as 
recyclable. The code then updates the counters in each 
file with the values that each class period has recycled
"""


import cv2 #Used to grayscale images/do all image processing
import picamera #Raspberry Pi camera module, used to take photos
import RPIO #Used to operate the servo through the Pi's GPIO pins
import time #Used to count objects collected on specific days
from PIL import Image #TODO Document
from RPIO import PWM #Used to operate the servo

#Initializes the servo so that it is centered
def initServo(servo):
    servo.set_servo(18, 1650)

#Takes an intensity value and classifies it as trash or recycling
def sortItem(intensity, servo):
    isRecyclable = 0

    print "Intensity: " + intensity #print out the intensity

    if intensity < 40: #Checks if the intensity meets the recyclable threshold
        print "TRASH"
        servo.set_servo(18, 1200) #Turn the servo to the left
    else:
        print "RECYCLABLE"
        isRecyclable = 1
        servo.set_servo(18, 2100) #Turn the servo to the right
	time.sleep(1)
    initServo(servo)
    return isRecyclable

def calculateIntensity():
    with picamera.PiCamera() as camera: #get access to the picamera
        camera.start_preview() #Show the image of the bottle
    	time.sleep(2) #Sleep so that there is time to take a picture
        camera.capture('item.jpg') #capture an image and store it to file item.jpg
        itemGray_img = cv2.imread('/home/pi/item.jpg',0) #read the image back in in gray scale
        itemIntensity = 0 
        itemMax = 0
        for x in range(500, 1250): #Scan over all x-values in the image
            for y in range (0, 1000): #Scan over y-values in the image
                itemIntensity = itemGray_img[y, x] #Calculate the intensity of the pixel being examined
                if itemIntensity > itemMax: #Calculate the max intensity
                    itemMax = itemIntensity     
        return itemMax


def main():
    servo = PWM.Servo() #Get access to the servo
    initServo(servo)
    
    period4count, period5count, period6count = getFileValues() #Get previous file counts

    while 1:
        raw_input() #Wait for the user to press "Enter
        stream = io.BytesIO() 
        highestIntensityPixel = calculateIntensity() #Get HIP for the image
        isRecyclable = sortItem(highestIntensityPixel, servo) #Sees if the item meets the recyclable threshold
            
    	time.sleep(1) #Give the servo time to drop off object in correct side of the bin
        initServo(servo)

main()

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


import cv2 #Used to grayscale images
import picamera #Used to take pictures
import io #TODO Document
import RPIO #Used to operate the servo
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

#Loads the number of objects that have previously been recycled
def getFileValues():
    #open counter files for reading
    period4 = open('/home/pi/period4.txt', 'r') 
    period5 = open('/home/pi/period5.txt', 'r') 
    period6 = open('/home/pi/period6.txt', 'r')

    #read the values from the file
    period4count = str(period4.read()) 
    period5count = str(period5.read())
    period6count = str(period6.read())

    #close the counter files
    period4.close()
    period5.close()
    period6.close()

    return period4count, period5count, period6count

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

def addToCounts(period4count, period5count, period6count):
        today = time.strftime("%A") #returns day of the week
        hour = time.strftime("%H") #returns hour of the day 0-23
        minute = time.strftime("%M") #returns minute of the hour 0-59
        ourtime = hour * 60 + minute #gives us the total minutes elapsed in the day
        time_init = 715 #the initial time for monday, tuesday, thursday, friday
        time_init_w = 725 #the initial time for wednesday
        range_m = 55 #class period length for monday friday
        range_t = 85 #class period length for tuesday thursday
        range_w= 80 #class period length for wednesday
        
        #Find what time of day it is to add to the counter of the specific class period
        if   (today == "Monday" or today == "Friday"):
            if   (ourtime >= time_init and 
               ourtime <= time_init + range_m):
                period4count += 1
            elif (ourtime >= time_init + 60 and
                  ourtime <= time_init + range_m + 60):
                period5count += 1
            elif (ourtime >= time_init + 120 and 
                  ourtime <= time_init + range_m + 120):
                period6count += 1
        elif (today == "Tuesday"):
            if   (ourtime >= time_init and 
                  ourtime <= time_init + range_t):
                period4count += 1
            elif (ourtime >= time_init + range_t + 5 and 
                  ourtime <= time_init + 2 * range_t + 5):
                period5count += 1
        elif (today == "Wednesday"):
            if   (ourtime >= time_init_w and 
                  ourtime <= time_init_w + range_w):
                period5count += 1
            elif (ourtime >= time_init_w + range_w + 5 and 
                  ourtime <= time_init_w + 2 * range_w + 5):
                period6count += 1
        elif (today == "Thursday"):
            if   (ourtime >= time_init and 
                  ourtime <= time_init + range_t):
                period4count += 1
            elif (ourtime >= time_init + range_t + 5 and 
                  ourtime <= time_init + 2 * range_t + 5):
                period6count += 1

        return period4count, period5count, period6count

        #Open the counter files
        period4 = open('/home/pi/period4.txt', 'w') 
        period5 = open('/home/pi/period5.txt', 'w') 
        period6 = open('/home/pi/period6.txt', 'w')

        #Write the new counts to the files
        period4.write(str(period4count)) 
        period5.write(str(period5count))
        period6.write(str(period6count))

        #Close the files
        period4.close()
        period5.close()
        period6.close()


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

        if (isRecyclable == 1): #If the object is recyclable, increment the counts
            period4count, period5count, period6count = addToCounts(period4count, period5count, period6count)

main()

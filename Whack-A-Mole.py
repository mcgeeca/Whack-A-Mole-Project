#!/usr/bin/env python3

#Author: Craig McGee Jr.
#Date: November 19, 2020
#Embedded Linux Final Project

import Adafruit_BBIO.GPIO as GPIO
import time
import blynklib
import os, sys
import random
import multiprocessing


# Stores header value to the LED variables
yellowLED = "P9_13"
blueLED = "P9_14"
greenLED = "P9_15"
redLED = "P9_16"

# Sets up all LEDs to be outputs
GPIO.setup(yellowLED, GPIO.OUT)
GPIO.setup(blueLED, GPIO.OUT)
GPIO.setup(greenLED, GPIO.OUT)
GPIO.setup(redLED, GPIO.OUT)

# Variable that is used to display score on Virtual 4
count = 0

# In this function a number is generated randomly.  1 is yellow, 2 is blue, 
# 3 is green, and 4 is red.  If the random number is generated then that light 
# corresponding to that number is turned on to which then it will stay on for 0.7
# seconds before turning off automatically.  It is important to note that this 
# will only run for 30 seconds.
def toggleLight():
    start_time = time.time()
    end_time = start_time + 30
    while time.time() < end_time:    
        num = random.randint(1,4)
        if(num == 1):
            GPIO.output(yellowLED, 1)
            time.sleep(0.7)
            GPIO.output(yellowLED, 0)
            time.sleep(0.7)
            
        elif(num == 2):
            GPIO.output(blueLED, 1)
            time.sleep(0.7)
            GPIO.output(blueLED, 0)
            time.sleep(0.7)
            
        elif(num == 3):
            GPIO.output(greenLED, 1)
            time.sleep(0.7)
            GPIO.output(greenLED, 0)
            time.sleep(0.7)
            
        else:
            GPIO.output(redLED, 1)
            time.sleep(0.7)
            GPIO.output(redLED, 0)
            time.sleep(0.7)
            
# This function is where the blynk app connection is setup as well as the 
# different corresponding buttons being pressed.  Also this is where the score
# you have is written to the display on Virtual 4.  It is important to note that
# this runs for exactly 34 seconds.  This is because, the countdown function 
# lasts 4 seconds and the toggleLight function lasts 30 seconds.  This ensures 
# that the blynk app disconnects when the game is over.
def blynkApp():

    # Get the autherization code (See setup.sh)
    BLYNK_AUTH = os.getenv('BLYNK_AUTH', default="")
    if(BLYNK_AUTH == ""):
        print("BLYNK_AUTH is not set")
        sys.exit()

    # Initialize Blynk
    blynk = blynklib.Blynk(BLYNK_AUTH)
    
    @blynk.handle_event('write V0')
    def my_write_handler_yellow_light(pin, value):
        global count
        if GPIO.input(yellowLED):
            GPIO.output(yellowLED, 0)
            count = count + 1
            blynk.virtual_write(4, count)

    @blynk.handle_event('write V1')
    def my_write_handler_blue_led(pin, value):
        global count
        if GPIO.input(blueLED):
            GPIO.output(blueLED, 0)
            count = count + 1
            blynk.virtual_write(4, count)

    
    @blynk.handle_event('write V2')
    def my_write_handler_green_led(pin, value):
        global count
        if GPIO.input(greenLED):
            GPIO.output(greenLED, 0)
            count = count + 1
            blynk.virtual_write(4, count)
    
    @blynk.handle_event('write V3')
    def my_write_handler_red_led(pin, value):
        global count
        if GPIO.input(redLED):
            GPIO.output(redLED, 0)
            count = count + 1
            blynk.virtual_write(4, count)
    
    
    start_time = time.time()
    end_time = start_time + 34
    while time.time() < end_time:
        blynk.run()

# This is the where the countdown sequence takes place.  Instead of the
# countdown starting from 5 seconds it starts at 4.  So each light represents a 
# second.  Yellow is 4, blue is 3, green is 2, and red is 1.  After red turns off
# the game begins by calling the toggleLight funciton
def countdown(): 
    GPIO.output(yellowLED, 1)
    time.sleep(1)
    GPIO.output(yellowLED, 0)
    GPIO.output(blueLED, 1)
    time.sleep(1)
    GPIO.output(blueLED, 0)
    GPIO.output(greenLED, 1)
    time.sleep(1)
    GPIO.output(greenLED, 0)
    GPIO.output(redLED, 1)
    time.sleep(1)
    GPIO.output(redLED, 0)
    
    toggleLight()

# These lines allow for the game and the blynk app to be ran in parallel.  This
# is done by using multiprocessing.
p1 = multiprocessing.Process(target=countdown)
p2 = multiprocessing.Process(target=blynkApp)

p1.start()
p2.start()

p1.join()
p2.join()
#!/usr/bin/env python3

import Adafruit_BBIO.GPIO as GPIO
import time
import blynklib
import os, sys
import random
import multiprocessing



yellowLED = "P9_13"
blueLED = "P9_15"
greenLED = "P9_16"
redLED = "P9_14"

GPIO.setup(yellowLED, GPIO.OUT)
GPIO.setup(blueLED, GPIO.OUT)
GPIO.setup(greenLED, GPIO.OUT)
GPIO.setup(redLED, GPIO.OUT)

count = 0

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
            
        
def blynkApp():
    BLYNK_AUTH='BqslJTRT5reIdaiUioBdgtzgW2ZCY8y7'

    # Initialize Blynk
    blynk = blynklib.Blynk(BLYNK_AUTH)
    
    @blynk.handle_event('write V0')
    def my_write_handler_yellow_light(pin, value):
        global count
        if GPIO.input(yellowLED):
            print('Current V{} value: {}'.format(pin, value[0]))
            GPIO.output(yellowLED, 0)
            count = count + 1
            blynk.virtual_write(4, count)

    @blynk.handle_event('write V1')
    def my_write_handler_blue_led(pin, value):
        global count
        if GPIO.input(blueLED):
            print('Current V{} value: {}'.format(pin, value[0]))
            GPIO.output(blueLED, 0)
            count = count + 1
            blynk.virtual_write(4, count)

    
    @blynk.handle_event('write V2')
    def my_write_handler_green_led(pin, value):
        global count
        if GPIO.input(greenLED):
            print('Current V{} value: {}'.format(pin, value[0]))
            GPIO.output(greenLED, 0)
            count = count + 1
            blynk.virtual_write(4, count)
    
    @blynk.handle_event('write V3')
    def my_write_handler_red_led(pin, value):
        global count
        if GPIO.input(redLED):
            print('Current V{} value: {}'.format(pin, value[0]))
            GPIO.output(redLED, 0)
            count = count + 1
            blynk.virtual_write(4, count)
    
    
    start_time = time.time()
    end_time = start_time + 34
    while time.time() < end_time:
        blynk.run()
        
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

p1 = multiprocessing.Process(target=countdown)
p2 = multiprocessing.Process(target=blynkApp)

p1.start()
p2.start()

p1.join()
p2.join()
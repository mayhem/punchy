#!/usr/bin/env python3
import sys
from time import sleep

import RPi.GPIO as GPIO

class SolenoidDriver:

    def __init__(self):
        self.solenoid_pin = 4
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.solenoid_pin, GPIO.OUT) # LED pin set as output

    def punch(self, duration):
        GPIO.output(self.solenoid_pin, GPIO.HIGH)
        sleep(duration / 1000)
        GPIO.output(self.solenoid_pin, GPIO.LOW)

if __name__ == "__main__":
    sd = SolenoidDriver()
    sd.punch(20)

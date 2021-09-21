# led.py

import RPi.GPIO as GPIO




# LED color setting
class IndicatorLED:
    def __init__(self, redPin = 12, greenPin = 19, bluePin = 13):
        #disable warnings (optional)
        GPIO.setwarnings(False)
        #Select GPIO Mode
        GPIO.setmode(GPIO.BCM)
        #set red,green and blue pins
        self.redPin = redPin
        self.greenPin = greenPin
        self.bluePin = bluePin
        #set pins as outputs
        GPIO.setup(self.redPin,GPIO.OUT)
        GPIO.setup(self.greenPin,GPIO.OUT)
        GPIO.setup(self.bluePin,GPIO.OUT)

        self.turnOff()

    def turnOff(self):
        GPIO.output(self.redPin,GPIO.LOW)
        GPIO.output(self.greenPin,GPIO.LOW)
        GPIO.output(self.bluePin,GPIO.LOW)

    def red(self):
        GPIO.output(self.redPin,GPIO.HIGH)
        GPIO.output(self.greenPin,GPIO.LOW)
        GPIO.output(self.bluePin,GPIO.LOW)

    def blue(self):
        GPIO.output(self.redPin,GPIO.LOW)
        GPIO.output(self.greenPin,GPIO.HIGH)
        GPIO.output(self.bluePin,GPIO.LOW)

    def green(self):
        GPIO.output(self.redPin,GPIO.LOW)
        GPIO.output(self.greenPin,GPIO.LOW)
        GPIO.output(self.bluePin,GPIO.HIGH)

    def updateColor(self, goalTemp, currTemp):
        if currTemp-goalTemp < -2:
            self.blue()
        elif currTemp-goalTemp > 2:
            self.red()
        else:
            self.green()


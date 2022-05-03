#tests.py

import time

from sensors import *
from smartplug import *
from fsm import *
from camera import *
from led import *


# Simple tests for the smartplug and sensors
def device_tests():

    print("\nRunning SmartPlug test:")
    try:
        plug = SmartPlug("192.168.1.115")
        plug.turnOff()
        time.sleep(1)

        plug.turnOn()
        time.sleep(1)

        plug.turnOff()
        time.sleep(1)

        print("SmartPlug PASSED")
    except Exception as e:
        print("SmartPlug FAILED")
        print(e)


    print("\nRunning TemperatureProbe test:")
    try:
        temp_probe = TemperatureProbe()
        print(temp_probe.getTemperature())
        print("TemperatureProbe PASSED")

    except Exception as e:
        print("TemperatureProbe FAILED")
        print(e)


    print("\nRunning HumiditySensor test:")
    try:
        humidity_sensor = HumiditySensor()
        print(humidity_sensor.getTemperature())
        print(humidity_sensor.getHumidity())

        print("HumiditySensor PASSED")

    except Exception as e:
        print("HumiditySensor FAILED")
        print(e)


    print("\nRunning IndicatorLED test:")
    try:
        led = IndicatorLED()
        led.turnOff()
        time.sleep(1)
        led.red()
        time.sleep(1)
        led.turnOff()
        time.sleep(1)
        led.green()
        time.sleep(1)
        led.turnOff()
        time.sleep(1)
        led.blue()
        time.sleep(1)
        led.turnOff()

        print("IndicatorLED (maybe) PASSED")

    except Exception as e:
        print(" FAILED")
        print(e)

device_tests()

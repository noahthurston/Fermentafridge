# main.py

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

# device_tests()


### ROUTINE CALLING CODE

# init
goalHumidity = 90
minHumidity = 80
maxHumidity = None

goalTemp = 88
minTemp = 86

humidifierIPAddrString = "192.168.1.115"
heaterIPAddrString = "192.168.1.148"

folderString = "/media/usb/{}".format(int(time.time()))


camera = Camera(folderString)

indicatorLED = IndicatorLED()

temperatureProbe = TemperatureProbe()
humiditySensor = HumiditySensor()

heaterPlug = SmartPlug(heaterIPAddrString)
humidiferPlug = SmartPlug(humidifierIPAddrString)

humidityFSM = HumidityFSM(goalHumidity, minHumidity, maxHumidity, humidiferPlug, verbose=True)
temperatureFSM = TemperatureFSM(goalTemp, minTemp, heaterPlug, verbose=True)


data_file = open("data.csv", "a")
data_file.write("\nepoch time, currProbeTemp, currAmbientTemp, currHumidity, humidityFSM.getState(), temperatureFSM.getState()")

currProbeTemp = 100
currAmbientTemp = 100
currHumidity = 100


maxIterations = 100000
for iteration in range(maxIterations):
    print("\n\nStarting iteration: {}".format(iteration))


    currProbeTemp = temperatureProbe.getTemperature()
    currAmbientTemp = humiditySensor.getTemperature()
    currHumidity = humiditySensor.getHumidity()
    
    print("probe: {:.2f}\tambient: {:.2f}\thumidity: {:.2f}".format(currProbeTemp, currAmbientTemp, currHumidity))

    humidityFSM.updateState(currHumidity)
    temperatureFSM.updateState(currProbeTemp, currAmbientTemp)

    data_file.write("\n{}, {:.2f}, {:.2f}, {:.2f}, {}, {}".format(time.time(), currProbeTemp, currAmbientTemp, currHumidity, humidityFSM.getState(), temperatureFSM.getState()))

    if iteration%50==0:
        camera.takePicture()

    indicatorLED.updateColor(goalTemp, currProbeTemp)


    time.sleep(5)


heaterPlug.turnOff()
humidiferPlug.turnOff

data_file.close()

#main.py

import time

from sensors import *
from smartplug import *
from fsm import *
from camera import *
from led import *

# init
goalHumidity = 75
minHumidity = 65
maxHumidity = None

goalTemp = 86
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

# maxIterations set to 100k, roughly 5.5 days
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

    if iteration%10==0:
        camera.takePicture()

    indicatorLED.updateColor(goalTemp, currProbeTemp)


    time.sleep(5)


heaterPlug.turnOff()
humidiferPlug.turnOff

data_file.close()

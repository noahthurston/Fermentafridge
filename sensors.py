# sensors.py

import time
import board
import adafruit_ahtx0
import glob

# Class for managing the temperature probe
class TemperatureProbe:

    def __init__(self, verbose=False):
        self.base_dir = '/sys/bus/w1/devices/'
        if verbose:
            print(glob.glob(self.base_dir + '28*'))
        self.device_folder = glob.glob(self.base_dir + '28*')[0]
        self.device_file = self.device_folder + '/w1_slave'

        self.old_temp = 100

    def read_temp_raw(self):
        f = open(self.device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def read_temp(self):
        lines = self.read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            return temp_c, temp_f

    # returns temperature in Fahrenheit
    def getTemperature(self):        
        try:
            temp_c, temp_f = self.read_temp()
            self.old_temp = temp_f
            return temp_f

        except Exception as e:
            print("ERROR: failed to get temperature from TemperatureProbe")
            print(e)
            return self.old_temp

        return temp_f


# Class for managing the wall mounted temperature and humidity sensor
class HumiditySensor:

    # while True:
    #     print(read_temp())
    #     print("\nTemperature: %0.1f C" % (sensor.temperature * 9.0 / 5.0 + 32.0))
    #     print("Humidity: %0.1f %%" % sensor.relative_humidity)

    #     time.sleep(1)

    def __init__(self):
        # Create sensor object, communicating over the board's default I2C bus
        # To pull values use sensor.temperature, sensor.relative_humidity
        i2c = board.I2C()  # uses board.SCL and board.SDA
        self.sensor = adafruit_ahtx0.AHTx0(i2c)

        self.old_temp = 100
        self.old_humidity = 100

    # returns temperature in Fahrenheit
    def getTemperature(self):
        try:
            temp = self.sensor.temperature*9.0/5.0+32.0
            self.old_temp = temp
            return temp

        except Exception as e:
            print("ERROR: failed to get temperature from HumiditySensor")
            print(e)
            return self.old_temp

    def getHumidity(self):
        try:
            humidity = self.sensor.relative_humidity
            self.old_humidity = humidity
            return humidity

        except Exception as e:
            print("ERROR: failed to get humidity from HumiditySensor")
            print(e)
            return self.old_humidity
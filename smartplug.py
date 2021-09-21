# smartplug.py

import kasa as k
import asyncio


# Class for managing the kasa smart plugs
class SmartPlug:

    # plug = k.SmartPlug("192.168.1.115")

    # def turn_on():
    #   asyncio.run(plug.turn_on())

    # def turn_off():
    #       asyncio.run(plug.turn_off())

    def __init__(self, ip_addr_string):
        self.ip_addr_string = ip_addr_string
        self.plug = k.SmartPlug(ip_addr_string)

    def turnOff(self):
        try:
            asyncio.run(self.plug.turn_off())
        except Exception as e:
            print("ERROR: failed to turn off outlet {}".format(self.ip_addr_string))
            print(e)

    def turnOn(self):
        try:
            asyncio.run(self.plug.turn_on())
        except Exception as e:
            print("ERROR: failed to turn on outlet {}".format(self.ip_addr_string))
            print(e)
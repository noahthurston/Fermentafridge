# camera.py

import time
import subprocess
from picamera import PiCamera


# Camera operator class
class Camera:
    def __init__(self, folder_string):
        # self.camera = PiCamera()

        self.folder_string = folder_string
        subprocess.run(["mkdir", folder_string])

    def takePicture(self, curr_time_str=None):
        curr_time_str = str(int(time.time())) if curr_time_str == None else curr_time_str
        subprocess.run(["raspistill", "-o", "{}/{}.png".format(self.folder_string, curr_time_str), "--nopreview"])

from time import *

import os
import platform
import subprocess
from driver_base import *
from network import *
import math

os.sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
import log

class DriverVisualizer(DriverNetwork):
    """Main driver for Visualizer UI (for testing)"""

    def __init__(self, num = 0, width = 0, height = 0, pixelSize = 15, port = 1618, stayTop = False):
        super(DriverVisualizer, self).__init__(num, width, height, host = "localhost", port = port)

        allip = False

        if self.width == 0 and self.height == 0:
            self.width = self.numLEDs
            self.height = 1

        if self.numLEDs != self.width * self.height:
            raise ValueError("Provide either num OR width and height, but not all three.")

        try:
            #check if there is already a visualizer open and send dummy packet
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self._host, self._port))
            s.send(bytearray([0,0,0])) 
            s.close()
        except:
            operating_system = platform.system().lower()
            suffix = ""
            if "windows" in operating_system:
                exe_string = "start python"
            elif "darwin" in operating_system:
                exe_string = "python"
                suffix = "&"
            else:
                exe_string = "python"
                suffix = "&"
                
            dname = os.path.dirname(os.path.abspath(__file__))
            script = '{}/visualizerUI.py'.format(dname)

            if allip: 
                ip = "--allip" 
            else: 
                ip = ""

            if stayTop:
                top = "--top"
            else:
                top = ""
            
            command = "{0} {1} --width {2} --height {3} --pixelsize {4} --port {5} {6} {7} {8}".format(exe_string, script, str(self.width), str(self.height), str(pixelSize), str(port), ip, top, suffix)
            #print command
            log.logger.debug(command)
            os.system(command)
            sleep(0.5)


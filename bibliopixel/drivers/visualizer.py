import time

import os
import platform
import subprocess
from network import DriverNetwork, socket
import math

from .. import log


class DriverVisualizer(DriverNetwork):
    """Main driver for Visualizer UI (for testing)"""

    def __init__(self, num=0, width=0, height=0, pixelSize=15, port=1618, stayTop=False):
        super(DriverVisualizer, self).__init__(
            num, width, height, host="localhost", port=port)

        allip = False

        if self.width == 0 and self.height == 0:
            self.width = self.numLEDs
            self.height = 1

        if self.numLEDs != self.width * self.height:
            raise ValueError(
                "Provide either num OR width and height, but not all three.")

        try:
            # check if there is already a visualizer open and send dummy packet
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self._host, self._port))
            s.send(bytearray([0, 0, 0]))
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

            command = "{0} {1} --width {2} --height {3} --pixelsize {4} --port {5} {6} {7} {8}".format(
                exe_string, script, str(self.width), str(self.height), str(pixelSize), str(port), ip, top, suffix)
            # print command
            log.debug(command)
            os.system(command)
            time.sleep(0.5)

MANIFEST = [
    {
        "id": "visualizer",
        "class": DriverVisualizer,
        "type": "driver",
        "display": "Visualizer",
        "desc": "Visualizer runs animations inside a simulator window.",
        "params": [{
                "id": "num",
                "label": "# Pixels",
                "type": "int",
                "default": 0,
                "min": 0,
                "help": "Total pixels in display. May use Width AND Height instead."
        }, {
            "id": "width",
            "label": "Width",
            "type": "int",
            "default": 0,
            "min": 0,
            "help": "Width of display. Set if using a matrix."
        }, {
            "id": "height",
            "label": "Height",
            "type": "int",
            "default": 0,
            "min": 0,
            "help": "Height of display. Set if using a matrix."
        }, {
            "id": "pixelSize",
            "label": "Pixel Size",
            "type": "int",
            "default": 15,
            "min": 5,
            "max": 50,
            "help": "Size of rendered pixels in UI."
        }, {
            "id": "port",
            "label": "Port",
            "type": "int",
            "default": 1618,
            "help": "Port to connect to/listen on. Only change if using multiple visualizers.",
            "group": "Advanced"
        },
            {
                "id": "stayTop",
                "label": "Stay on Top",
                "type": "bool",
                "default": False,
                "help": "Force Visualizer UI to stay on top of all other windows.",
        }]
    }
]

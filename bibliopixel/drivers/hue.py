from driver_base import DriverBase
from .. import log

try:
    from phue import Bridge
except:
    error = "Unable to import phue. Please install. pip install phue"
    log.error(error)
    raise ImportError(error)

import colorsys


class DriverHue(DriverBase):

    def __init__(self, num, ip, nameMap=None):
        super(DriverHue, self).__init__(num)

        if nameMap and len(nameMap) != self.numLEDs:
            raise ValueError(
                "nameMap must have the same number of entries as the number of LEDs.")

        self._bridge = Bridge(ip)
        self._bridge.connect()
        self._transitionTime = 0
        self._brightness = 254

        if nameMap:
            self._lights = self._bridge.get_light_objects('name')
            self._ids = nameMap
        else:
            self._lights = self._bridge.get_light_objects('id')
            self._ids = [l for l in self._lights]

        if len(self._lights) < self.numLEDs:
            raise ValueError(
                "More LEDs were specified than there are available Hue lights.")

        self.setTransitionTime(0)  # start with no transition time

    def setMasterBrightness(self, brightness):
        if brightness < 0 or brightness > 255:
            raise ValueError("Brightness value must be between 0 and 255")
        self._brightness = brightness

        return True

    def setTransitionTime(self, time):
        if time < 0.0 or time > 30.0:
            raise ValueError(
                "Transition time must be between 0.0 and 30.0 seconds.")

        self._transitionTime = int(time * 10)

    def _mapRange(self, value, minFrom, maxFrom, minTo, maxTo):
        return minTo + (maxTo - minTo) * ((value - minFrom) / (maxFrom - minFrom))

    def _rgb2hs(self, rgb):
        r = rgb[0] / 255.0
        g = rgb[1] / 255.0
        b = rgb[2] / 255.0

        h, s, v = colorsys.rgb_to_hsv(r, g, b)

        h = int(self._mapRange(h, 0.0, 1.0, 0, 65535))
        s = int(self._mapRange(s, 0.0, 1.0, 0, 254))
        return (h, s)

    def update(self, data):
        pixels = [tuple(data[(p * 3):(p * 3) + 3])
                  for p in range(len(data) / 3)]

        for i in range(len(self._ids)):
            h, s = self._rgb2hs(pixels[i])
            bri = self._brightness
            if s == 0:
                bri = 0

            cmd = {'on': s != 0, 'bri': bri, 'hue': h, 'saturation': s,
                   'transitiontime': self._transitionTime}
            self._bridge.set_light(self._ids[i], cmd)

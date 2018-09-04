from . driver_base import DriverBase
from .. util import log

try:
    from phue import Bridge
except:
    error = "Unable to import phue. Please install. pip install phue"
    log.error(error)
    raise ImportError(error)

import colorsys


class Hue(DriverBase):
    """
    Driver for interacting with Philips Hue lights.

    Provides the same parameters of :py:class:`.driver_base.DriverBase` as
    well as those below:

    :param str ip: Network hostname or IP address of the Hue base.
    :param list nameMap: List of names to map to each pixel index
    """

    def __init__(self, num, ip, nameMap=None, **kwds):
        super().__init__(num, **kwds)

        if nameMap and len(nameMap) != self.numLEDs:
            raise ValueError(
                "nameMap must have the same number of entries as the number "
                "of LEDs.")

        self._bridge = Bridge(ip)
        self._bridge.connect()
        self._transitionTime = 0

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

    def setTransitionTime(self, time):
        if time < 0.0 or time > 30.0:
            raise ValueError(
                "Transition time must be between 0.0 and 30.0 seconds.")

        self._transitionTime = int(time * 10)

    def _mapRange(self, value, minFrom, maxFrom, minTo, maxTo):
        return minTo + (maxTo - minTo) * (value - minFrom) / (maxFrom - minFrom)

    def _rgb2hs(self, rgb):
        r = rgb[0] / 255.0
        g = rgb[1] / 255.0
        b = rgb[2] / 255.0

        h, s, v = colorsys.rgb_to_hsv(r, g, b)

        h = int(self._mapRange(h, 0.0, 1.0, 0, 65535))
        s = int(self._mapRange(s, 0.0, 1.0, 0, 254))
        return (h, s)

    def _send_packet(self):
        for i in range(len(self._ids)):
            h, s = self._rgb2hs(self._colors[i + self._pos])
            bri = min(254, self._brightness)
            if s == 0:
                bri = 0

            cmd = {'on': s != 0, 'bri': bri, 'hue': h, 'saturation': s,
                   'transitiontime': self._transitionTime}
            self._bridge.set_light(self._ids[i], cmd)


from .. util import deprecated
if deprecated.allowed():  # pragma: no cover
    DriverHue = Hue

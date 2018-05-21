from ... util.colors import gamma
from .. channel_order import ChannelOrder
from . base import SPIBase


class APA102(SPIBase):
    """Driver for APA102/SK9822 based LED strips on devices like
    the Raspberry Pi and BeagleBone

    Provides the same parameters as
    :py:class:`bibliopixel.drivers.SPI.SPIBase`
    """

    def __init__(self, num, gamma=gamma.APA102, **kwargs):
        super().__init__(num, gamma=gamma, **kwargs)

        # APA102/SK9822 requires latch bytes at the end)
        # Many thanks to this article for combined APA102/SK9822 protocol
        # https://cpldcpu.com/2016/12/13/sk9822-a-clone-of-the-apa102/
        self._start_frame = 4  # start frame is [0, 0, 0, 0]
        self._pixel_bytes = self.numLEDs * 4  # 4 byte frames [bright, r, g, b]
        self._pixel_stop = self._start_frame + self._pixel_bytes
        self._reset_frame = 4  # for SK9822 [0, 0, 0, 0]
        self._end_frame = (num // 2) + 1
        self._packet = self.maker.bytes(self._start_frame + self._pixel_bytes +
                                        self._reset_frame + self._end_frame)

        self.set_device_brightness(0xFF)  # required to setup _packet

    def set_device_brightness(self, val):
        """
        APA102 & SK9822 support on-chip brightness control, allowing greater
        color depth.

        APA102 superimposes a 440Hz PWM on the 19kHz base PWM to control
        brightness. SK9822 uses a base 4.7kHz PWM but controls brightness with a
        variable current source.

        Because of this SK9822 will have much less flicker at lower levels.
        Either way, this option is better and faster than scaling in
        BiblioPixel.
        """
        # bitshift to scale from 8 bit to 5
        self._chipset_brightness = (val >> 3)
        self._brightness_list = [0xE0 + self._chipset_brightness] * self.numLEDs
        self._packet[self._start_frame:self._pixel_stop:4] = (
            self._brightness_list)

    def _compute_packet(self):
        self._render()
        self._packet[self._start_frame + 1:self._pixel_stop:4] = self._buf[0::3]
        self._packet[self._start_frame + 2:self._pixel_stop:4] = self._buf[1::3]
        self._packet[self._start_frame + 3:self._pixel_stop:4] = self._buf[2::3]

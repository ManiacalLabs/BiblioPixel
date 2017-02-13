import time

from .. import log
from . import update_thread


class ThreadStrategy(object):
    def __init__(self, enabled, led):
        self.enabled = enabled
        self.led = led
        self.use_animation_thread = False
        self.animation_thread = None
        self.waiting_brightness = None

        if enabled:
            self.update_thread = update_thread.UpdateThread(led.drivers)
            self.update_thread.start()

    def update_colors(self):
        if self.enabled:
            self.update_thread.update_colors()
        else:
            for d in self.led.drivers:
                d.update_colors()
            for d in self.led.drivers:
                d.sync()

    def wait_for_update(self):
        if self.enabled:
            while all([d._thread.sending() for d in self.led.drivers]):
                time.sleep(0.000001)

    def set_brightness(self, brightness):
        """Sets the master brightness scaling, 0 - 255

        If the driver supports it the brightness will be sent to the receiver
        directly.
        """
        if brightness > 255 or brightness < 0:
            raise ValueError('Brightness must be between 0 and 255')

        if self.use_animation_thread:
            self.waiting_brightness = brightness
        else:
            self.led._do_set_brightness(brightness)

    def push_to_driver(self):
        """Push the current pixel state to the driver"""
        self.wait_for_update()
        if self.waiting_brightness is not None:
            self.led.do_set_brightness(self.waiting_brightness)
            self.waiting_brightness = None
        self.update_colors()

    def set_animation(self, animation):
        self.animation = animation

    def report_framerate(self, start, mid, now):
        stepTime = int(mid - start)
        if self.enabled:
            updateTime = int(self.led.lastThreadedUpdate())
            log.debug(
                "Frame: %sms / Update Max: %sms", stepTime, updateTime)
        else:
            updateTime = int(now - mid)
            totalTime = stepTime + updateTime
            log.debug("%sms/%sfps / Frame: %sms / Update: %sms",
                      totalTime, int(1000 / max(totalTime, 1)), stepTime,
                      updateTime)

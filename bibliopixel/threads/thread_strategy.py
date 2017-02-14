import threading, time

from .. import log
from . import update_thread


class ThreadStrategy(object):
    """
    ThreadStrategy handles threading - and eventually multiprocessing - for
    BaseAnimation and LEDBase.

    It would be better if this were two separate classes but some functionality
    requires information from both sides... I mark these with an XXX below.
    """

    def __init__(self, use_update_thread, led):
        self.use_update_thread = use_update_thread
        self.use_animation_thread = False
        self.led = led
        self.animation_thread = None
        self.animation_stop_event = threading.Event()

        self.waiting_brightness = None

        if use_update_thread:
            self.update_thread = update_thread.UpdateThread(led.drivers)
            self.update_thread.start()

    def update_colors(self):
        if self.use_update_thread:
            self.update_thread.update_colors()
        else:
            for d in self.led.drivers:
                d.update_colors()
            for d in self.led.drivers:
                d.sync()

    def wait_for_update(self):
        if self.use_update_thread:
            while all([d._thread.sending() for d in self.led.drivers]):
                time.sleep(0.000001)

    def set_brightness(self, brightness):
        """Sets the master brightness scaling, 0 - 255

        If the driver supports it the brightness will be sent to the receiver
        directly.
        """
        # XXX: This is called from the LED's update cycle, but uses animation
        # thread information.
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
            self.led._do_set_brightness(self.waiting_brightness)
            self.waiting_brightness = None
        self.update_colors()

    def set_animation(self, animation):
        self.animation = animation

    def report_framerate(self, start, mid, now):
        # XXX: this is called from the animation's update cycle, but uses LED
        # thread information.
        stepTime = int(mid - start)
        if self.use_update_thread:
            updateTime = int(self.led.lastThreadedUpdate())
            log.debug(
                "Frame: %sms / Update Max: %sms", stepTime, updateTime)
        else:
            updateTime = int(now - mid)
            totalTime = stepTime + updateTime
            log.debug("%sms/%sfps / Frame: %sms / Update: %sms",
                      totalTime, int(1000.0 / max(totalTime, 1)), stepTime,
                      updateTime)

    def stop_animation_thread(self, wait=False):
        if self.animation_thread:
            self.animation_stop_event.set()

            if wait:
                self.animation_thread.join()

    def animation_stopped(self):
        return not (self.animation_thread and self.animation_thread.isAlive())

    def animation_wait(self, t):
        if self.use_animation_thread:
            self.animation_stop_event.wait(t)
        else:
            time.sleep(t)

    def run_animation(self, run, threaded, join_thread):
        self.use_animation_thread = threaded
        if self.use_animation_thread:
            self.animation_stop_event.clear()

            def target():
                # TODO: no testpath exercises this code...
                log.debug('Starting thread...')
                run()
                log.debug('Thread Complete')

            self.animation_thread = threading.Thread(target=target, daemon=True)
            self.animation_thread.start()
            if join_thread:
                self.animation_thread.join()
        else:
            run()

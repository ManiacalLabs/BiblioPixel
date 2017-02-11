from . import update_thread


class ThreadStrategy(object):
    def __init__(self, enabled, led):
        self.enabled = enabled
        self.led = led
        self.animation_threads = False

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

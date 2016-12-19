from . importer import make_object


class Project(object):
    def __init__(self, driver, led, animation, run):
        self.drivers = [make_object(**driver)]
        self.led = make_object(self.drivers, **led)
        self.animation = make_object(self.led, **animation)
        self.run = lambda: self.animation.run(**run)

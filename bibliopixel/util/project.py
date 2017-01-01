import sys
from . importer import make_object
from . read_dict import read_dict


class Project(object):
    def __init__(self, driver, led, animation, run):
        self.drivers = [make_object(**driver)]
        self.led = make_object(self.drivers, **led)
        self.animation = make_object(self.led, **animation)
        self.run = lambda: self.animation.run(**run)


def run(data):
    return Project(**read_dict(data)).run()


if __name__ == '__main__':
    run(*sys.argv[1:])

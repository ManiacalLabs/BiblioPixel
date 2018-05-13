try:
    import curses as _curses
except:
    _curses = None

import itertools, os, queue, weakref
from . driver_base import DriverBase


class Curses(DriverBase):
    """
    A driver that uses the "curses" library to get a colored display on a
    regular terminal.

    Note that this driver only works on some platforms.

    The Linux default terminal probably works, but the exact details depend
    on your specific OS and version.

    The MacOS default (Terminal) works at low frame rates but the colors are
    wrong (I delved into it and we can't work round it).

    However, in the MacOS Term2 program, it works at framerates up to at least
    10fps.

    TODO: check how it works on the Rpi (#803)
    """
    DRIVERS = weakref.WeakSet()

    def __init__(self, *args, column_width=3, char='●', **kwds):
        super().__init__(*args, **kwds)

        if not (self.width or self.height):
            self.width = self.numLEDs
            self.height = 1

        if list(Curses.DRIVERS):
            raise ValueError('More than one Curses driver is not allowed')

        Curses.DRIVERS.add(self)

        self.column_width = column_width
        self.offset = column_width // 2
        self.char = chr(char) if isinstance(char, int) else char
        self.queue = queue.Queue()

    def _send_packet(self):
        self.queue.put(True)

    def stop(self):
        super().stop()
        self.queue.put(False)

    @staticmethod
    def main():
        """
        If a project has a Curses driver, the section "main" in the section
        "run" must be "bibliopixel.drivers.curses.Curses.main".

        """
        if not _curses:
            # https://stackoverflow.com/a/1325587/43839
            if os.name == 'nt':
                raise ValueError('curses is not supported under Windows')
            raise ValueError('Your platform does not support curses.')
        try:
            driver = next(iter(Curses.DRIVERS))
        except:
            raise ValueError('No Curses driver in project')

        _curses.wrapper(driver.run_in_curses)

    def run_in_curses(self, stdscr):
        self.set_curses_colors()
        stdscr.clear()
        stdscr.refresh()
        cy, cx = stdscr.getmaxyx()
        cx //= self.column_width
        height, width = self.height, self.width

        if width > cx:
            # log.warning('Width %d too wide for screen %d', width, cx)
            width = cx

        if height > cx:
            # log.warning('Height %d too tall for screen %d', height, cy)
            height = cy

        while self.queue.get():
            for x in range(width):
                for y in range(height):
                    self.write_color(stdscr, x, y)

            stdscr.refresh()

    def write_color(self, stdscr, x, y):
        red, green, blue = self._colors[self._pos + x + self.width * y]
        r, g, b = red >> 5, green >> 5, blue >> 6
        index = r + 8 * (g + 8 * b)
        pair = _curses.color_pair(index)
        screen_x = self.column_width * x + self.offset

        # Pair 0 always has foreground white; just draw a background if so.
        char = self.char if index else ' '
        stdscr.addch(y, screen_x, char, pair)

    @staticmethod
    def set_curses_colors():
        s = 1000 / 255
        for r, g, b in itertools.product(range(8), range(8), range(4)):
            index = r + 8 * (g + 8 * b)
            # Color 0 is black and can't be changed.
            # Pair 0 is white on black and can't be changed.
            if index:
                r, g, b = r << 5, g << 5, b << 6
                _curses.init_color(index, int(r * s), int(g * s), int(b * s))
                _curses.init_pair(index, index, 0)

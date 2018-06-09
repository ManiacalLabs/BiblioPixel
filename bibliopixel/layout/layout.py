import copy, time
from .. import util
from .. project import attributes, data_maker, fields
from .. util.threads.update_threading import UpdateThreading
from .. util.color_list import to_triplets


class Layout(object):
    """
    Base Layer class. Use Strip, Matrix, Cube, or Circle instead!

    :param drivers: A list of drivers
    :param threadedUpdate: If True, updates to this layout are done in a
        separate thread
    :param brightness: An initial brightness value from 0 to 255
    :param maker: A data maker to make color_lists. TODO: Link to what a maker
        is.
    :param color_list: If non-Null, the layout uses this color_list instead
        of creating its own

    :ivar int numLEDs: Total number of pixels held by this layout instance
    """

    CLONE_ATTRS = 'maker', 'brightness'

    pre_recursion = fields.default_converter

    @classmethod
    def construct(cls, project, **desc):
        """Construct a layout.
        SHOULD BE PRIVATE
        """
        return cls(project.drivers, maker=project.maker, **desc)

    def __init__(self, drivers, threadedUpdate=False, brightness=255,
                 maker=data_maker.MAKER, color_list=None, **kwds):
        attributes.set_reserved(self, 'layout', **kwds)
        self.drivers = drivers if isinstance(drivers, list) else [drivers]
        self.maker = maker

        # self._colors will always be the same list - i.e. is guaranteed only
        # to be changed by list surgery, never assignment.
        if color_list is None:
            if not hasattr(self, 'numLEDs'):
                self.numLEDs = sum(d.numLEDs for d in self.drivers)
            self._colors = maker.color_list(self.numLEDs)
        else:
            self.numLEDs = len(color_list)
            self._colors = color_list

        pos = 0
        for d in self.drivers:
            d.set_colors(self._colors, pos)
            pos += d.numLEDs

        self.frame_render_time = 0
        self.animation_sleep_time = None

        self.threading = UpdateThreading(threadedUpdate, self)
        self.brightness = brightness
        self.set_brightness(brightness)

    def set_pixel_positions(self, pixel_positions):
        """SHOULD BE PRIVATE"""
        for d in self.drivers:
            d.set_pixel_positions(pixel_positions)

    def update(self):
        """DEPRECATED: Use :py:func:`push_to_driver` instead"""
        util.deprecated.deprecated('Layout.update')
        return self.push_to_driver()

    def start(self):
        for d in self.drivers:
            d.start()

    def stop(self):
        self.threading.stop()
        for d in self.drivers:
            d.stop()

    def join(self, timeout=None):
        self.threading.wait()
        for d in self.drivers:
            d.join(timeout)

    def cleanup_drivers(self):
        for d in self.drivers:
            d.cleanup()

    def cleanup(self):
        self.all_off()
        try:
            self.push_to_driver()
        except:
            pass
        self.threading.wait_for_update()

    def clone(self):
        """
        Return an independent copy of this layout with a completely separate
        color_list and no drivers.
        """
        args = {k: getattr(self, k) for k in self.CLONE_ATTRS}
        args['color_list'] = copy.copy(self.color_list)
        return self.__class__([], **args)

    @property
    def shape(self):
        """
        Return a tuple indicating the dimensions of the layout - (x,) for a
        strip, (x, y) for an array, (x, y, z) for a cube, and
        (ring_count, ring_steps) for a circle.
        """
        raise NotImplementedError

    @property
    def dimensions(self):
        util.deprecated.deprecated('Layout.dimensions')
        return self.shape

    @property
    def color_list(self):
        return self._colors

    @color_list.setter
    def color_list(self, color_list):
        self.set_color_list(color_list)

    def set_color_list(self, color_list, offset=0):
        """
        Set the internal colors starting at an optional offset.

        If `color_list` is a list or other 1-dimensional array, it is reshaped
        into an N x 3 list.

        If `color_list` too long it is truncated; if it is too short then only
        the initial colors are set.
        """
        if not len(color_list):
            return
        color_list = to_triplets(color_list)

        size = len(self._colors) - offset
        if len(color_list) > size:
            color_list = color_list[:size]
        self._colors[offset:offset + len(color_list)] = color_list

    def _get_base(self, pixel):
        if pixel >= 0 and pixel < self.numLEDs:
            return self._colors[pixel]
        return 0, 0, 0  # don't go out of bounds

    def _set_base(self, pixel, color):
        if pixel >= 0 and pixel < self.numLEDs:
            if isinstance(color, str):
                color = util.colors.COLORS[color]
            else:
                color = tuple(color)
            self.color_list[pixel] = color

    def get_pixel_positions(self):
        result = []
        for x in range(len(self.numLEDs)):
            result.append([x, 0, 0])
        return result

    def push_to_driver(self):
        """Push the current pixel state to the driver"""
        # This is overridden elsewhere.
        self.threading.push_to_driver()

    def set_brightness(self, brightness):
        self.brightness = brightness
        for d in self.drivers:
            d.set_brightness(brightness)

    # Set single pixel to RGB value
    def setRGB(self, pixel, r, g, b):
        """Set single pixel using individual RGB values instead of tuple"""
        self._set_base(pixel, (r, g, b))

    def setHSV(self, pixel, hsv):
        """Set single pixel to HSV tuple"""
        color = util.colors.hsv2rgb(hsv)
        self._set_base(pixel, color)

    # turns off the desired pixel
    def setOff(self, pixel):
        """Set single pixel off"""
        self._set_base(pixel, (0, 0, 0))

    def all_off(self):
        """Set all pixels off"""
        self._colors[:] = [(0, 0, 0)] * self.numLEDs

    # Fill the strand (or a subset) with a single color using a Color object
    def fill(self, color, start=0, end=-1):
        """Fill the entire strip with RGB color tuple"""
        start = max(start, 0)
        if end < 0 or end >= self.numLEDs:
            end = self.numLEDs - 1
        for led in range(start, end + 1):  # since 0-index include end in range
            self._set_base(led, color)

    # Fill the strand (or a subset) with a single color using RGB values
    def fillRGB(self, r, g, b, start=0, end=-1):
        """Fill entire strip by giving individual RGB values instead of tuple"""
        self.fill((r, g, b), start, end)

    # Fill the strand (or a subset) with a single color using HSV values
    def fillHSV(self, hsv, start=0, end=-1):
        """Fill the entire strip with HSV color tuple"""
        self.fill(util.colors.hsv2rgb(hsv), start, end)


class MultiLayout(Layout):
    CLONE_ATTRS = Layout.CLONE_ATTRS + ('gen_coord_map', 'coord_map')

    def __init__(self, *args, gen_coord_map=None, coord_map=None, **kwds):
        super().__init__(*args, **kwds)
        self.gen_coord_map = gen_coord_map
        if gen_coord_map:
            if coord_map:
                util.log.warning('Cannot set both coord_map and gen_coord_map')
            elif isinstance(gen_coord_map, dict):
                coord_map = self.gen_multi(**gen_coord_map)
            else:
                coord_map = self.gen_multi(gen_coord_map)
        self.coord_map = coord_map

    def gen_multi(self, *args, **kwds):
        raise NotImplementedError

    def set_colors(self, buf):
        """
        DEPRECATED: use self.color_list

        Use with extreme caution!
        Directly sets the internal buffer and bypasses all brightness and
        rotation control buf must also be in the exact format required by the
        display type.
        """
        util.deprecated.deprecated('layout.set_colors')
        if len(self._colors) != len(buf):
            raise IOError("Data buffer size incorrect! "
                          "Expected: {} bytes / Received: {} bytes"
                          .format(len(self._colors), len(buf)))
        self._colors[:] = buf

    def setBuffer(self, buf):
        util.deprecated.deprecated('layout.setBuffer')
        self.color_list = buf

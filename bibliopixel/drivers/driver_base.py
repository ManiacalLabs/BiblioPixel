from . channel_order import ChannelOrder
from .. util.colors import gamma as _gamma
from .. project import attributes, data_maker, fields
import threading, time


class DriverBase(object):
    """
    Base driver class to build other drivers from.

    :param int num: Number of total pixels held by this driver

    :param int width: Width of matrix, for use
        with :py:class:`bibliopixel.layout.matrix.Matrix`

    :param int height: Height of matrix, for use
        with :py:class:`bibliopixel.layout.matrix.Matrix`

    :param str c_order: Color channel order

    :param gamma: Gamma correction table. Preset tables available
        in :py:mod:`bibliopixel.util.colors.gamma`
    """

    # If set_device_brightness is not empty, it's a method that allows you
    # to directly set the brightness for the device.
    #
    # If it is empty, then the brightness is used as a scale factor in rendering
    # the pixels.
    set_device_brightness = None

    pre_recursion = fields.default_converter

    @classmethod
    def construct(cls, project, **desc):
        """Construct a driver from a project and a description."""
        return cls(maker=project.maker, **desc)

    def __init__(self, num=0, width=0, height=0, c_order="RGB",
                 gamma=None, maker=data_maker.MAKER, **kwds):
        attributes.set_reserved(self, 'driver', **kwds)

        if num == 0:
            num = width * height
            if num == 0:
                raise ValueError("Either num, or width and height are needed!")

        self.numLEDs = num
        gamma = gamma or _gamma.DEFAULT
        self.gamma = gamma

        if isinstance(c_order, str):
            c_order = ChannelOrder.make(c_order)

        self.c_order = c_order
        self.perm = ChannelOrder.ORDERS.index(c_order)

        self.pixel_positions = None

        self.width = width
        self.height = height
        self.maker = maker
        self._buf = self._make_buffer()

        self.lastUpdate = 0
        self.brightness_lock = threading.Lock()
        self._brightness = 255
        self._waiting_brightness = None
        self.time = time.time

    def set_pixel_positions(self, pixel_positions):
        """
        Internal Use Only

        Placeholder callback for sending physical pixel layout data to the
        ``SimPixel`` driver.
        """
        pass

    def set_colors(self, colors, pos):
        """
        Use with caution!

        Directly set the pixel buffers.

        :param colors: A list of color tuples
        :param int pos: Position in color list to begin set operation.
        """
        self._colors = colors
        self._pos = pos

        end = self._pos + self.numLEDs
        if end > len(self._colors):
            raise ValueError('Needed %d colors but found %d' % (
                end, len(self._colors)))

    def set_project(self, project):
        self.project = project
        self.time = project.time

    def start(self):
        """
        Called right before this driver will run.  This is the place
        to do things like start threads, not in the constructor.
        """

    def stop(self):
        """
        Called to request any threads or resources to shut down.
        """

    def cleanup(self):
        """
        Called to shut this driver down, and stop all threads and processes.
        """

    def join(self, timeout=None):
        """
        Called to join threads.
        """

    def bufByteCount(self):
        """
        Total number of bytes that the pixel buffer represents.
        Mainly used for drivers such as :py:mod:`bibliopixel.drivers.serial`
        and :py:mod:`.network`
        """
        return 3 * self.numLEDs

    def sync(self):
        """

        The sync() method is called after the entire frame has been
        sent to the device to indicate that it may now be displayed.

        This is particularly useful when there are multiple drivers comprising
        one display which all need to display the next frame at exactly the same
        time.
        """

    def _compute_packet(self):
        """Compute the packet from the colors and position.

        Eventually, this will run on the compute thread.
        """

    def _send_packet(self):
        """Send the packet to the driver.

        Eventually, this will run on an I/O thread.
        """

    def update_colors(self):
        """Apply any corrections to the current color list
        and send the results to the driver output. This function primarily
        provided as a wrapper for each driver's implementation of
        :py:func:`_compute_packet` and :py:func:`_send_packet`.
        """
        start = self.time()

        with self.brightness_lock:
            # Swap in a new brightness.
            brightness, self._waiting_brightness = (
                self._waiting_brightness, None)

        if brightness is not None:
            self._brightness = brightness
            if self.set_device_brightness:
                self.set_device_brightness(brightness)

        self._compute_packet()
        self._send_packet()

        self.lastUpdate = self.time() - start

    def set_brightness(self, brightness):
        """Set the global brightness for this driver's output.

        :param int brightness: 0-255 value representing the desired
            brightness level
        """
        with self.brightness_lock:
            self._waiting_brightness = brightness

    def _render(self):
        """Typically called from :py:func:`_compute_packet` this applies
        brightness and gamma correction to the pixels controlled by this
        driver.
        """
        if self.set_device_brightness:
            level = 1.0
        else:
            level = self._brightness / 255.0
        gam, (r, g, b) = self.gamma.get, self.c_order
        for i in range(min(self.numLEDs, len(self._buf) / 3)):
            c = [int(level * x) for x in self._colors[i + self._pos]]
            self._buf[i * 3:(i + 1) * 3] = gam(c[r]), gam(c[g]), gam(c[b])

    def _make_buffer(self):
        return self.maker.bytes(self.bufByteCount())

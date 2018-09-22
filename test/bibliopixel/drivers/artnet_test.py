import struct, unittest
from bibliopixel.util import artnet_message, udp
from bibliopixel.util.colors import printer
from bibliopixel.animation import tests as animation_tests
from test.bibliopixel import mark_tests
from test.bibliopixel.project import make
from test.bibliopixel.util import udp_test
from bibliopixel.drivers import artnet

LOCALHOST = '127.0.0.1'
ADDRESS = LOCALHOST, artnet_message.UDP_PORT
MAX_STEPS = 3

PROJECT = {
    "driver": "artnet",
    "shape": 12,
    "animation": ".tests.StripChannelTest",
    "run": {
        "max_steps": MAX_STEPS
    }
}


class DMXMessageTest(unittest.TestCase):
    @mark_tests.long_test
    @mark_tests.fails_in_travis
    @mark_tests.fails_on_windows
    def test_blackout(self):
        results = []
        with udp_test.receive_udp(ADDRESS, results, MAX_STEPS + 1):
            project = make.make_project(PROJECT)
            project.start()

        self.assertEqual(len(results), MAX_STEPS + 1)

        make_msg = artnet_message.DMXMessage.from_buffer_copy

        failures = []
        blackout = make_msg(results.pop())
        for i, result in enumerate(results):
            actual = make_msg(result)
            expected = artnet_message.dmx_message()

            for j, color in enumerate(animation_tests.BASE_COLORS):
                expected.data[3 * j:3 * (j + 1)] = color

            for j in range(7, 10):
                color = animation_tests.CYCLE_COLORS[i]
                expected.data[3 * j:3 * (j + 1)] = color

            for j, (e, a) in enumerate(zip(expected.data, actual.data)):
                if e != a:
                    failures.append((i, j, e, a))

        self.assertEqual(failures, [])
        self.assertEqual(bytes(blackout), bytes(artnet_message.dmx_message()))

    def _make_driver_and_copy(self, numLEDs, offset=0):
        driver = artnet.ArtNet(numLEDs, offset=offset)
        driver._buf[:] = (i % 256 for i in range(len(driver._buf)))
        driver._copy_buffer_into_data()
        return list(driver._buf), list(driver.msg.data)

    def test_big(self):
        buffer, data = self._make_driver_and_copy(500)
        self.assertEqual(buffer[:len(data)], data)

    def test_little(self):
        buffer, data = self._make_driver_and_copy(8)
        self.assertEqual(buffer, data[:len(buffer)])

    def test_big_offset(self):
        buffer, data = self._make_driver_and_copy(500, 4)
        self.assertEqual(buffer[4:4 + len(data)], data)

    def test_little_offset(self):
        buffer, data = self._make_driver_and_copy(8, 4)
        split_point = len(buffer) - 4
        self.assertEqual(buffer[4:], data[:split_point])
        self.assertTrue(all(d == 0 for d in data[split_point:]))

    def test_big_offset_negative(self):
        buffer, data = self._make_driver_and_copy(500, -4)
        self.assertEqual(buffer[4:4 + len(data)], data)

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
    "driver": {
        "typename": "artnet",
        "ip_address": LOCALHOST
    },
    "shape": 12,
    "animation": ".tests.StripChannelTest",
    "run": {
        "max_steps": MAX_STEPS
    }
}


class DMXMessageTest(unittest.TestCase):
    @mark_tests.long_test
    @mark_tests.travis_test
    def test_blackout(self):
        results = []
        with udp_test.receive_udp(ADDRESS, results, MAX_STEPS + 1):
            project = make.make_project(PROJECT)
            project.start()

        self.assertEquals(len(results), MAX_STEPS + 1)

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

        self.assertEquals(failures, [])
        self.assertEquals(bytes(blackout), bytes(artnet_message.dmx_message()))

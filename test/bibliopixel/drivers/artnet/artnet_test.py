import struct, unittest
from bibliopixel.util import udp
from bibliopixel.util.colors import printer
from bibliopixel.animation import tests as animation_tests
from test.bibliopixel import mark_tests
from test.bibliopixel.project import make
from test.bibliopixel.util import udp_test
from bibliopixel.drivers.artnet import artnet, dmx_message

LOCALHOST = '127.0.0.1'
ADDRESS = LOCALHOST, artnet.UDP_PORT
MAX_STEPS = 3

PROJECT = {
    "driver": {
        "typename": ".artnet.artnet",
        "ip_address": LOCALHOST
    },
    "dimensions": 12,
    "animation": ".tests.StripChannelTest",
    "run": {
        "max_steps": MAX_STEPS
    }
}


class DMXMessageTest(unittest.TestCase):
    @mark_tests.long_test
    def test_blackout(self):
        results = []
        with udp_test.receive_udp(ADDRESS, results):
            project = make.make_project(PROJECT)
            project.start()

        self.assertEquals(len(results), MAX_STEPS + 1)

        make_msg = dmx_message.Message.from_buffer_copy

        failures = []
        blackout = make_msg(results.pop())
        for i, result in enumerate(results):
            actual = make_msg(result)
            expected = dmx_message.dmx_message()

            for j, color in enumerate(animation_tests.BASE_COLORS):
                expected.data[3 * j:3 * (j + 1)] = color

            for j in range(7, 10):
                color = animation_tests.CYCLE_COLORS[i]
                expected.data[3 * j:3 * (j + 1)] = color

            for j, (e, a) in enumerate(zip(expected.data, actual.data)):
                if e != a:
                    failures.append((i, j, e, a))

        self.assertEquals(failures, [])
        self.assertEquals(bytes(blackout), bytes(dmx_message.dmx_message()))

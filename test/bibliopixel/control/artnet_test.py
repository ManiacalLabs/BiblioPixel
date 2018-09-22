import os, time, queue, unittest
from bibliopixel.control import artnet
from bibliopixel.util import artnet_message, data_file, udp
from .. project import make
from .. import mark_tests
from test.bibliopixel.util import udp_test


class ArtNetControlTest(unittest.TestCase):
    @mark_tests.fails_in_travis
    @mark_tests.fails_on_windows
    def test_artnet_control(self):
        project = make_project(ARTNET_CONTROL)
        q = queue.Queue()
        project.test_callback = q.put
        project.controls[0].set_root(project)
        sender = udp.QueuedSender(SEND_ADDRESS)

        with project.controls[0].run_until_stop(), sender.run_until_stop():
            sender.send(OUTGOING_MESSAGE)
            results = q.get(timeout=3)

        self.assertEqual(results, TEST_DATA)

    @mark_tests.fails_in_travis
    @mark_tests.fails_on_windows
    def test_artnet_integration(self):
        sender = udp.QueuedSender(SEND_ADDRESS)
        receiver = udp.QueuedReceiver(RECEIVE_ADDRESS)
        project = make_project(ARTNET_PROJECT)

        with sender.run_until_stop(), receiver.run_until_stop():
            project.start()
            time.sleep(0.01)
            sender.queue.put(OUTGOING_MESSAGE)
            get = receiver.queue.get
            result = [get(), get(), get()]

        msgs = [artnet_message.bytes_to_message(i) for i in result]
        data = [m.data for m in msgs]
        self.assertEqual(len(msgs), 3)
        self.assertTrue(not any(data[0]))
        self.assertTrue(not any(data[2]))
        actual = bytearray(data[1])

        # We expect to lose the last two bytes because we have uneven sizes.
        # TODO: perhaps we should round UP instead of DOWN?
        self.assertEqual(actual[:-2], TEST_DATA[:-2])
        self.assertEqual(actual[-2], 0)
        self.assertEqual(actual[-1], 0)

    def offset_test(self, offset):
        control = artnet.ArtNet(offset=offset)
        msg = artnet_message.dmx_message()
        msg.data[:] = [i % 256 for i in range(len(msg.data))]
        result = control._convert(bytes(msg))
        return list(msg.data), list(result['data'])

    def test_offset_positive(self):
        data, result = self.offset_test(4)
        self.assertEqual(result, [0, 0, 0, 0] + data[:-4])

    def test_offset_negative(self):
        data, result = self.offset_test(-4)
        self.assertEqual(result, data[4:] + [0, 0, 0, 0])


def make_project(f):
    data = data_file.loads(f, '.yml')
    return make.make_project(data)


ROOT_DIR = os.path.dirname(__file__)
TEST_DATA = bytearray(range(256)) + bytearray(range(256))
OUTGOING_MESSAGE = artnet_message.dmx_message(data=TEST_DATA)
PIXEL_COUNT = len(TEST_DATA) // 3

ARTNET_PORT = artnet_message.UDP_PORT
ALTERNATE_PORT = ARTNET_PORT + 1
SEND_ADDRESS = '', ARTNET_PORT
RECEIVE_ADDRESS = '', ALTERNATE_PORT


ARTNET_CONTROL = """
shape: 1

animation: animation

controls:
  typename: artnet
  pre_routing: ".test_callback()"
  extractor:
    omit: [type, net, subUni]
  verbose: True

run:
  threaded: true
""".format(**globals())


ARTNET_PROJECT = """
shape: {PIXEL_COUNT}

animation: animation

controls:
  typename: artnet
  port: {ARTNET_PORT}

  extractor:
    omit: [net, subUni]

  routing:
    dmx: animation.color_list

  verbose: True

driver:
  typename: artnet
  port: {ALTERNATE_PORT}

run:
  fps: 10
  max_steps: 3
  threaded: true
""".format(**globals())

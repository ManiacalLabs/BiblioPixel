import contextlib, queue, time, unittest
from .. import mark_tests

from bibliopixel.util import udp

TEST_ADDRESS = '127.0.0.1', 5678
TIMEOUT = 0.1


@contextlib.contextmanager
def receive_udp(address, results, expected):
    receiver = udp.QueuedReceiver(address)
    with receiver.run_until_stop():
        yield

    results.extend(receiver.queue.get() for i in range(expected))
    try:
        receiver.queue.get(timeout=TIMEOUT)
    except queue.Empty:
        pass
    else:
        raise ValueError


class UDPTest(unittest.TestCase):
    @mark_tests.fails_in_travis
    def test_full(self):
        messages = [s.encode() for s in ('foo', '', 'bar', 'baz', '', 'bing')]
        expected = [s for s in messages if s]
        # Note that empty messages are either not sent, or not received.

        actual = []
        with receive_udp(TEST_ADDRESS, actual, len(expected)):
            sender = udp.QueuedSender(TEST_ADDRESS)
            sender.start()
            for m in messages:
                sender.send(m)
        self.assertEqual(actual, expected)
        # TODO: if I don't have something here, this hangs!
        time.sleep(0.001)

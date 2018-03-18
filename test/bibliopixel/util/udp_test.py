import contextlib, queue, time, unittest

from bibliopixel.util import udp

TEST_ADDRESS = '127.0.0.1', 5678
TIMEOUT = 0.3


@contextlib.contextmanager
def receive_udp(address, results):
    receiver = udp.QueuedReceiver(address)
    receiver.start()

    yield

    try:
        while True:
            results.append(receiver.queue.get(timeout=TIMEOUT))
    except queue.Empty:
        pass


class UDPTest(unittest.TestCase):
    def test_full(self):
        messages = [s.encode() for s in ('foo', '', 'bar', 'baz', '', 'bing')]
        expected = [s for s in messages if s]
        # Note that empty messages are either not sent, or not received.

        actual = []
        with receive_udp(TEST_ADDRESS, actual):
            sender = udp.QueuedSender(TEST_ADDRESS)
            sender.start()
            for m in messages:
                sender.send(m)

        self.assertEquals(actual, expected)

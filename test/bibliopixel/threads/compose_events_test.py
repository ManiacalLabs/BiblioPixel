import threading, unittest

from bibliopixel.util.threads import compose_events


class ComposeEventTest(unittest.TestCase):
    def test_compose_events(self):
        a, b = threading.Event(), threading.Event()
        master = compose_events.compose_events([a, b])
        self.assertFalse(master.is_set())
        a.set()
        self.assertFalse(master.is_set())
        b.set()
        self.assertTrue(master.is_set())
        a.clear()
        self.assertFalse(master.is_set())
        b.clear()
        self.assertFalse(master.is_set())
        b.set()
        self.assertFalse(master.is_set())
        a.set()
        self.assertTrue(master.is_set())

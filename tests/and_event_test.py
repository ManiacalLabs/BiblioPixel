import threading, unittest

from bibliopixel import and_event


class AndEventTest(unittest.TestCase):
    def do_test(self, ander):
        a, b = threading.Event(), threading.Event()
        master = ander([a, b])
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

    def test_and_event(self):
        self.do_test(and_event.AndEvent)

    def test_compose_events(self):
        self.do_test(and_event.compose_events)

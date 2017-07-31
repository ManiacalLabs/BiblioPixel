import functools, time, unittest
from bibliopixel.threads import sub

WAIT_FOR_SUB = 0.1


def pause(delay=0.005):
    time.sleep(delay)


def run(input, output, *arg, **kwds):
    pause()

    if arg != (1, 2, 3):
        raise ValueError('1 2 3')

    if kwds != dict(a=1):
        raise ValueError('a=1')

    pause()


class SubTest(unittest.TestCase):
    def do_test(self, use_subprocess):
        s, i, o = sub.run(run, 1, 2, 3, a=1, use_subprocess=use_subprocess)
        self.assertTrue(s.is_alive())
        pause()
        self.assertTrue(s.is_alive())

        pause(WAIT_FOR_SUB)
        self.assertFalse(s.is_alive())

    def test_subprocess(self):
        self.do_test(True)

    def test_threading(self):
        self.do_test(False)

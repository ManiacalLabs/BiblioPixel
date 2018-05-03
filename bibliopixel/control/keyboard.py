import getpass, platform, sys, threading
from .. util import log
from . control import ExtractedControl

# See https://stackoverflow.com/questions/42603000
DARWIN_ROOT_WARNING = """
In MacOS, pynput must to be running as root in order to get keystrokes.

Try running your program like this:

    sudo %s <your commands here>
"""

INSTALL_ERROR = """
Please install the pynput library with

    $ pip install pynput

"""


try:
    import pynput

except ImportError:
    pynput = Listener = None

else:
    class Listener(pynput.keyboard.Listener):
        def join(self, timeout=None):
            # join() on pynput.keyboard.Listener waits on a queue...
            self._queue.put(None)
            return super().join(timeout)


def keyname(key):
    return getattr(key, 'name', None) or getattr(key, 'char')


class Keyboard(ExtractedControl):
    EXTRACTOR = {
        'keys_by_type': {
            'press': ['type', 'key'],
            'release': ['type', 'key'],
        },

        'normalizers': {
            'key': keyname,
        },
    }

    def _press(self, key):
        self.receive({'type': 'press', 'key': key})

    def _release(self, key):
        self.receive({'type': 'release', 'key': key})

    def _make_thread(self):
        if not pynput:
            raise ValueError(INSTALL_ERROR)

        if platform.platform().startswith('Darwin'):
            if getpass.getuser() != 'root':
                log.warning(DARWIN_ROOT_WARNING, sys.argv[0])

        log.info('Starting to listen for keyboard input')
        return Listener(self._press, self._release)

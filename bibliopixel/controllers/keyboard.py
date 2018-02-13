import getpass, platform, sys
from .. util import log
from . controls import ExtractedControls

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


def keyname(key):
    return getattr(key, 'name', None) or getattr(key, 'char')


class Keyboard(ExtractedControls):
    EXTRACTOR = {
        'keys_by_type': {
            'press': ['type', 'key'],
            'release': ['type', 'key'],
        },

        'normalizers': {
            'key': keyname,
        },
    }

    def _make_thread(self):
        try:
            import pynput
        except Exception as e:
            e.args = (INSTALL_ERROR,) + e.args
            raise

        if platform.platform().startswith('Darwin'):
            if getpass.getuser() != 'root':
                log.warning(DARWIN_ROOT_WARNING, sys.argv[0])

        return pynput.keyboard.Listener(
            lambda key: self.receive({'type': 'press', 'key': key}),
            lambda key: self.receive({'type': 'release', 'key': key}))


class KeyboardTester:
    def __setattr__(self, k, v):
        super().__setattr__(k, v)
        print(k, '=', v)


def test_keyboard():
    keyboard = Keyboard(routing={'press': 'press', 'release': 'release'})
    keyboard.start(KeyboardTester())
    keyboard.thread.join()


if __name__ == '__main__':
    test_keyboard()

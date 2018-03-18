import getpass, platform, sys
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
        try:
            import pynput
        except Exception as e:
            e.args = (INSTALL_ERROR,) + e.args
            raise

        if platform.platform().startswith('Darwin'):
            if getpass.getuser() != 'root':
                log.warning(DARWIN_ROOT_WARNING, sys.argv[0])

        return pynput.keyboard.Listener(self._press, self._release)


class KeyboardTester:
    def __setattr__(self, k, v):
        super().__setattr__(k, v)
        log.printer(k, '=', v)


def main():
    keyboard = Keyboard(routing={'press': 'press', 'release': 'release'})
    keyboard.start(KeyboardTester())
    keyboard.thread.join()


if __name__ == '__main__':
    main()

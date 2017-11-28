Class BaseGamePad
=================

GamePad classes are supported by
[[BaseGameAnim\|Animations#basegameanim]] to allow handling interactive
input into the animation. [SerialGamePad\|#class-serialgamepad] and
[WinGamePadEmu\|#class-wingamepademu] are provided in BiblioPixel but
custom drivers can be written by inheriting from BaseGamePad located in
bibliopixel.gamepad

\_\_init\_\_
^^^^^^^^^^^^

Must be overridden by inheriting class.

getKeys
^^^^^^^

Must be overridden by inheriting class and return a dictionary of key
states, see below. Automatically called by
[[BaseGameAnim.handleKeys()\|Animations#basegameanim]]

.. code:: python

    #example return value
    {
        "A": True,
        "B": False,
        "START": False,
        "SELECT": False,
        "LEFT": True,
        "RIGHT": True,
        "UP": True,
        "DOWN": True,
    }

Using the above dictionary return value method is intended to ensure
that game animations can handle the output of any input device once it
is properly wrapped in a BaseGamePad inheriting driver class.

close
^^^^^

Override if special handling needs to be done when finished with the
class instance. All BaseGamePad inheriting classes support the python
"with" construct and this will automatically be called when leaving the
scope.

Class WinGamePadEmu
===================

Located at bibliopixel.win\_gamepad\_emu, this GamePad driver is mainly
intended for testing by globally hooking into the system keyboard
events, since BiblioPixel does have a window to handle input. `Python
for Windows Extensions <http://sourceforge.net/projects/pywin32/>`__
must be installed for this to function.

\_\_init\_\_
^^^^^^^^^^^^

(btn\_map)

-  **btn\_map** - A dictionary mapping output names to keyboard keys. By
   default, this uses the arrow keys for D-Pad input and Enter="START",
   SpaceBar="SELECT", A="A", S="B", Z="X", and X="Y". Defined like this:

.. code:: python

    {
        "UP": win32con.VK_UP,
        "DOWN": win32con.VK_DOWN,
        "LEFT": win32con.VK_LEFT,
        "RIGHT": win32con.VK_RIGHT,
        "SELECT": win32con.VK_SPACE,
        "START": win32con.VK_RETURN,
        "A": "A",
        "B": "S",
        "X": "Z",
        "Y": "X"
    }

The dictionary key is the key that will be used in the getKeys() output
and the value is the keyboard button that will be bound to that
dictionary key. Standard characters can be specified by a string
containing that character. Other keys can use the win32con values:

.. code:: python

    KEYMAP = {
        "enter": win32con.VK_RETURN,
        "up": win32con.VK_UP,
        "down": win32con.VK_DOWN,
        "left": win32con.VK_LEFT,
        "right": win32con.VK_RIGHT,
        "backspace": win32con.VK_BACK,
        "delete": win32con.VK_DELETE,
        "end": win32con.VK_END,
        "home": win32con.VK_HOME,
        "tab": win32con.VK_TAB,
        "f1": win32con.VK_F1,
        "f2": win32con.VK_F2,
        "f3": win32con.VK_F3,
        "f4": win32con.VK_F4,
        "f5": win32con.VK_F5,
        "f6": win32con.VK_F6,
        "f7": win32con.VK_F7,
        "f8": win32con.VK_F8,
        "f9": win32con.VK_F9,
        "f10": win32con.VK_F10,
        "f11": win32con.VK_F11,
        "f12": win32con.VK_F11,
        "pageup": win32con.VK_PRIOR,
        "pagedown": win32con.VK_NEXT,
        "escape": win32con.VK_ESCAPE
        }

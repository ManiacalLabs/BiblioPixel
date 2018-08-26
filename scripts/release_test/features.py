import getpass, os, platform

# This is a list of MIDI ports that are automatically added and don't show
# that the user actually has a hardware MIDI device connected.
MIDI_PORTS_TO_REMOVE = {'IAC Driver Bus 1'}

# https://raspberrypi.stackexchange.com/questions/5100
IS_WINDOWS = not getattr(os, 'uname', None)
IS_RASPBERRY_PI = not IS_WINDOWS and os.uname()[4].startswith('arm')
IS_MAC = platform.platform().startswith('Darwin')
IS_ROOT = getpass.getuser() == 'root'

ALL_PIXEL_ID = '1D50:60AB'
ALL_PIXEL_BAUD = 921600


def get_all_pixel():
    from bibliopixel.drivers.serial.devices import Devices
    devices = Devices(ALL_PIXEL_ID, ALL_PIXEL_BAUD)
    devs = sorted(devices.find_serial_devices().items())
    return devs and devs[0]


class Feature:
    @staticmethod
    def keyboard():
        return (not IS_MAC) or IS_ROOT

    @staticmethod
    def all_pixel():
        return bool(get_all_pixel())

    @staticmethod
    def browser():
        return not IS_RASPBERRY_PI

    @staticmethod
    def j12k():
        return False

    @staticmethod
    def midi():
        import mido
        return set(mido.get_input_names()) - MIDI_PORTS_TO_REMOVE

    @staticmethod
    def windows():
        return IS_WINDOWS


FEATURES = set(k for k in dir(Feature) if not k.startswith('_'))


def check_features(features):
    missing = features - FEATURES
    if missing:
        raise ValueError('Do not understand features ' + ', '.join(missing))


def get_features():
    features = set()

    for feature in FEATURES:
        checker = getattr(Feature, feature)
        try:
            if checker():
                features.add(feature)
        except:
            pass

    return features

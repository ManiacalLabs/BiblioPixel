from .. util import log


class RETURN_CODES:
    SUCCESS = 255  # All is well
    REBOOT = 42  # Device reboot needed after configuration
    ERROR = 0  # Generic error
    ERROR_SIZE = 1  # Data received does not match given command length
    ERROR_UNSUPPORTED = 2  # Unsupported command
    ERROR_PIXEL_COUNT = 3  # Too many pixels for device
    ERROR_BAD_CMD = 4  # Unknown Command


RETURN_CODE_ERRORS = {
    RETURN_CODES.SUCCESS: 'Success!',
    RETURN_CODES.REBOOT: 'Device reboot needed after configuration.',
    RETURN_CODES.ERROR: 'Generic error',
    RETURN_CODES.ERROR_SIZE: 'Data packet size incorrect.',
    RETURN_CODES.ERROR_UNSUPPORTED: 'Unsupported configuration attempted.',
    RETURN_CODES.ERROR_PIXEL_COUNT: 'Wrong number of pixels for device.',
    RETURN_CODES.ERROR_BAD_CMD:
        'Unsupported protocol command. Check your device version.',
}


class BiblioSerialError(Exception):
    pass


def print_error(error):
    msg = RETURN_CODE_ERRORS.get(error, 'Unknown error occured.')
    log.error('%s: %s', error, msg)


def raise_error(error):
    raise BiblioSerialError(print_error(error))

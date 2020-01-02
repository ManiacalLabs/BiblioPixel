import serial
from ... drivers.return_codes import RETURN_CODES
from ... util import log, util


def send_packet(cmd, size, dev, baudrate, timeout, more_data=None):
    packet = util.generate_header(cmd, size)
    if more_data:
        packet.append(more_data)

    com = serial.Serial(dev, baudrate=baudrate, timeout=timeout)
    com.write(packet)
    code = read_byte(com)
    ok = (code == RETURN_CODES.SUCCESS)
    return com, code, ok


def read_byte(com):
    try:
        resp = com.read(1)
        if resp:
            return ord(resp)
    except Exception:
        log.exception('Serial exception in read')

import ctypes, functools
from . import log

DMX_LENGTH = 512
ARTNET_DMX = 0x5000
ARTNET_VERSION = 14
NAME = b'Art-Net\x00'
MAX_NET = 0xFF
MAX_SUBNET = 0xF
MAX_UNIVERSE = 0xF
UDP_PORT = 0x1936  # 6454


@functools.lru_cache(maxsize=DMX_LENGTH)
def MessageClass(length=DMX_LENGTH):
    assert 0 <= length <= DMX_LENGTH
    assert length % 2 == 0, 'artnet only takes messages of even length'

    Char, Int8, Int16 = ctypes.c_char, ctypes.c_ubyte, ctypes.c_ushort

    class DMXMessage(ctypes.Structure):
        # http://artisticlicence.com/WebSiteMaster/User%20Guides/art-net.pdf p47
        _fields_ = [
            ('id', Char * 8),
            ('opCode', Int16),
            ('protVerHi', Int8),
            ('protVerLo', Int8),
            ('sequence', Int8),
            ('physical', Int8),
            ('subUni', Int8),
            ('net', Int8),
            ('lengthHi', Int8),
            ('length', Int8),
            ('data', Int8 * length),  # At position 18
        ]

    return DMXMessage


def dmx_message(
        length=None, net=0, subnet=0, universe=0, sequence=1, data=None):
    if length is None:
        length = DMX_LENGTH if (data is None) else len(data)
    elif data is not None:
        assert len(data) == length

    Message = MessageClass(length)

    assert 0 <= sequence <= DMX_LENGTH
    assert 0 <= net <= MAX_NET
    assert 0 <= subnet <= MAX_SUBNET
    assert 0 <= universe <= MAX_UNIVERSE

    # http://artisticlicence.com/WebSiteMaster/User%20Guides/art-net.pdf p5
    subUni = (subnet << 4) + universe
    hi, lo = divmod(length, 256)

    msg = Message(
        id=NAME,
        opCode=ARTNET_DMX,
        protVerLo=ARTNET_VERSION,
        sequence=sequence,
        net=net,
        subUni=subUni,
        lengthHi=hi,
        length=lo)

    if data is not None:
        msg.data[:] = data

    return msg


DMXMessage = MessageClass()
EMPTY_MESSAGE_SIZE = ctypes.sizeof(MessageClass(0))


def bytes_to_message(b):
    if not isinstance(b, bytearray):
        b = bytearray(b)

    length = len(b) - EMPTY_MESSAGE_SIZE
    assert 0 <= length <= DMX_LENGTH

    result = MessageClass(length).from_buffer(b)
    if result.id == NAME[:-1]:
        return result
    # For some reason, ctypes throws away that trailing \0 character
    # when converting back to bytes().
    log.error('Expected name %s but got name %s', NAME[:-1], result.id)

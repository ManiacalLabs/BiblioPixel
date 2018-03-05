import ctypes

DMX_LENGTH = 512
ARTNET_DMX = 0x5000
ARTNET_VERSION = 14
NAME = 'Art-Net\x00'
MAX_NET = 0xFF
MAX_SUBNET = 0xF
MAX_UNIVERSE = 0xF


def dmx_message(data=None, length=None, net=0, subnet=0, universe=0,
                sequence=1):
    if length is None:
        if data is None:
            length = DMX_LENGTH
        else:
            length = len(data)

    assert length % 2 == 0, 'artnet only takes messages of even length'
    assert 0 <= length <= DMX_LENGTH
    assert 0 <= sequence <= DMX_LENGTH
    assert 0 <= net <= MAX_NET
    assert 0 <= subnet <= MAX_SUBNET
    assert 0 <= universe <= MAX_UNIVERSE

    Char, Int8, Int16 = ctypes.c_char, ctypes.c_ubyte, ctypes.c_ushort

    class ArtnetDMXMessage(ctypes.Structure):
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

    # http://artisticlicence.com/WebSiteMaster/User%20Guides/art-net.pdf p5
    subUni = (subnet << 4) + universe
    hi, lo = divmod(length, 256)

    msg = ArtnetDMXMessage(
        id=NAME.encode(),
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


Message = type(dmx_message())

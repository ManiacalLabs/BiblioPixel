import struct, unittest

from bibliopixel.util.artnet_message import dmx_message


class DMXMessageTest(unittest.TestCase):
    def do_test(self, data, sequence=1, **kwds):
        msg = dmx_message(data=data, sequence=sequence, **kwds)
        original = Original(data, sequence, **kwds).broadcast()
        self.assertEqual(len(bytes(msg)), len(original))

        differences = []
        for i, (a, b) in enumerate(zip(bytes(msg), original)):
            if a != b:
                differences.append((i, a, b))

        self.assertEqual(bytes(msg), original)

    def test_blackout(self):
        self.do_test(bytes(512 * [0]))

    def test_trivial(self):
        self.do_test(bytes())

    def test_ramp_and_a_half(self):
        self.do_test(bytes(i % 256 for i in range(384)))


class Original:
    def __init__(self, dmxdata, packet_counter=1, net=0, subnet=0, universe=0):
        self.dmxdata = dmxdata
        self.packet_counter = packet_counter
        self.net = net
        self.subnet = subnet
        self.universe = universe

    def broadcast(self):
        # New Array
        data = []
        # Fix ID 7byte + 0x00
        data.append("Art-Net\x00")
        # OpCode = OpOutput / OpDmx -> 0x5000, Low Byte first
        data.append(struct.pack('<H', 0x5000))
        # ProtVerHi and ProtVerLo -> Protocol Version 14, High Byte first
        data.append(struct.pack('>H', 14))
        # Order 1 to 255
        data.append(struct.pack('B', self.packet_counter))
        self.packet_counter += 1
        if self.packet_counter > 255:
            self.packet_counter = 1
        # Physical Input Port
        data.append(struct.pack('B', 0))
        # Artnet source address
        data.append(
            struct.pack('<H', self.net << 8 | self.subnet << 4 | self.universe))
        # Length of DMX Data, High Byte First
        data.append(struct.pack('>H', len(self.dmxdata)))
        # DMX Data
        for d in self.dmxdata:
            data.append(struct.pack('B', d))
        # convert from list to string
        result = bytes()
        for token in data:
            try:  # Handels all strings
                result = result + token.encode('utf-8', 'ignore')
            except:  # Handels all bytes
                result = result + token

        return result

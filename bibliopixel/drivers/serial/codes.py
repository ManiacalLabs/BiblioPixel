from enum import IntEnum


class CMDTYPE(IntEnum):
    SETUP_DATA = 1  # config data (LED type, SPI speed, num LEDs)
    PIXEL_DATA = 2  # raw pixel data will be sent as [R1,G1,B1,R2,G2,B2,...]
    BRIGHTNESS = 3  # data will be single 0-255 brightness value, length must be 0x00,0x01
    GETID = 4
    SETID = 5
    GETVER = 6
    SYNC = 7


class LEDTYPE(IntEnum):
    GENERIC = 0  # Use if the serial device only supports one chipset
    LPD8806 = 1
    WS2801 = 2
    # These are all the same
    WS2811 = 3
    WS2812 = 3
    WS2812B = 3
    NEOPIXEL = 3
    APA104 = 3
    # 400khz variant of above
    WS2811_400 = 4

    TM1809 = 5
    TM1804 = 5
    TM1803 = 6
    UCS1903 = 7
    SM16716 = 8
    APA102 = 9
    LPD1886 = 10
    P9813 = 11


SPIChipsets = [
    LEDTYPE.LPD8806,
    LEDTYPE.WS2801,
    LEDTYPE.SM16716,
    LEDTYPE.APA102,
    LEDTYPE.P9813
]

# Chipsets here require extra pixels padded at the end
# Key must be an LEDTYPE
# value a lambda function to calc the value based on numLEDs
BufferChipsets = {
    LEDTYPE.APA102: lambda num: (int(num / 64.0) + 1)
}

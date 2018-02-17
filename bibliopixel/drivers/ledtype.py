from enum import IntEnum


class LEDTYPE(IntEnum):
    """Enumerated LED type names to be used with
    :py:mod:`bibliopixel.drivers.serial` and
    :py:mod:`bibliopixel.drivers.SPI`
    """
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
    SK9822 = 9
    LPD1886 = 10
    P9813 = 11

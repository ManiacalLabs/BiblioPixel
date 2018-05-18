"""
Configure the AllPixel or similar module
"""

import signal, sys
from .. drivers.serial.codes import LEDTYPE
from .. drivers.return_codes import BiblioSerialError
from .. util import log

types = [
    [LEDTYPE.GENERIC, 'GENERIC'],
    [LEDTYPE.LPD8806, 'LPD8806'],
    [LEDTYPE.WS2801, 'WS2801 '],
    [LEDTYPE.NEOPIXEL, 'WS2812/NEOPIXEL'],
    [LEDTYPE.APA104, 'APA104'],
    [LEDTYPE.WS2811_400, 'WS2811_400'],
    [LEDTYPE.TM1809, 'TM1809/TM1804'],
    [LEDTYPE.TM1803, 'TM1803 '],
    [LEDTYPE.UCS1903, 'UCS1903'],
    [LEDTYPE.SM16716, 'SM16716'],
    [LEDTYPE.APA102, 'APA102/DOTSTAR'],
    [LEDTYPE.LPD1886, 'LPD1886'],
    [LEDTYPE.P9813, 'P9813']
]


def get_input(msg):
    return input('\n' + msg)


def get_int(msg, invalid=-1):
    v = get_input(msg)
    try:
        return int(v)
    except:
        return invalid


def showSelectList(msg, values):
    log.printer('\n' + msg)
    shift = len(str(len(values)))
    count = 0
    for v in values:
        log.printer('{}: {}'.format(str(count).rjust(shift), v))
        count += 1
    return get_int('Choice: ')


def run(args):
    from ..drivers.serial.driver import Serial
    from ..drivers.serial.devices import Devices
    from ..drivers.serial.codes import SPIChipsets

    try:
        log.printer('Press Ctrl+C anytime to quit.')

        log.printer('\nScanning for devices...')
        devices = Devices(args.hardware_id, args.baud)
        devs = sorted(devices.find_serial_devices().items())
        d = ''
        if not devs:
            get_input(
                'No devices found! Please connect one and press any key...')
            raise ValueError()
        if len(devs) == 1:
            d = devs[0][1]
        else:
            d = showSelectList('Select device:', devs)
            if d < 0 or d >= len(devs):
                log.printer('\nInvalid choice!')
                raise ValueError()
            d = devs[d][1]

        t = showSelectList('Choose LED Type', [v[1] for v in types])
        if t < 0 or t >= len(types):
            log.printer('\nInvalid choice!')
            raise ValueError()
        t = types[t]

        num = get_int('Number of LEDs: ', invalid=0)
        if num <= 0:
            log.printer('\nInvalid choice!')
            raise ValueError()

        spi = 2
        use_spi = t[0] in SPIChipsets
        if use_spi:
            spi = get_int('SPI Speed (1-24): ', invalid=0)
            if spi <= 0:
                log.printer('\nInvalid choice!')
                raise ValueError()

        details = 'Device: {}\nLED Type: {}\nNum LEDs: {}'.format(d, t[1], num)
        if use_spi:
            details += '\nSPI Speed: {}'.format(spi)

        log.printer('\n' + details + '\n')

        try:
            Serial(t[0], num, dev=d, SPISpeed=spi, restart_timeout=6)
            log.printer('\nConfigure complete!')
        except BiblioSerialError as e:
            log.printer('\nError configuring device!')

    except KeyboardInterrupt:
        sys.exit(128 + signal.SIGINT)
    except ValueError as e:
        pass


def set_parser(parser):
    parser.set_defaults(run=run)
    parser.add_argument('--hardware-id', default='1D50:60AB',
                        help='USB Vendor ID : Product ID of device. '
                             'Defaults to VID:PID for AllPixel')
    parser.add_argument('--baud', default=921600, type=int,
                        help='Serial baud rate.')

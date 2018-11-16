"""
Find serial devices and update serial device IDs
"""

from .. util import log

CONNECT_MESSAGE = """
Connect just one Serial device (AllPixel) and press enter..."""


def run(args):
    from ..drivers.serial.driver import Serial
    from ..drivers.serial.devices import Devices
    import serial

    run = True
    log.printer("Press Ctrl+C any time to exit.")
    try:
        while run:
            try:
                input(CONNECT_MESSAGE)
                devices = Devices(args.hardware_id, args.baud)
                ports = devices.find_serial_devices()
                if not ports:
                    log.printer("No serial devices found. Please connect one.")
                    continue

                port = sorted(ports.items())[0][1][0]
                id = devices.get_device_id(port)
                log.printer("Device ID of {}: {}".format(port, id))
                newID = input("Input new ID (enter to skip): ")
                if newID != '':
                    try:
                        newID = int(newID)
                        if newID < 0 or newID > 255:
                            raise ValueError()

                        devices.set_device_id(port, newID)
                        id = devices.get_device_id(port)
                        log.printer("Device ID set to: %s" % id)
                    except ValueError:
                        log.printer("Please enter a number between 0 and 255.")
            except serial.SerialException as e:
                log.printer("Problem connecting to serial device. %s" % e)

            except Exception as e:
                log.printer('Programmer error with exception %s' % e)

    except KeyboardInterrupt:
        pass


def set_parser(parser):
    parser.set_defaults(run=run)
    parser.add_argument('--hardware-id', default='1D50:60AB',
                        help='USB Vendor ID : Product ID of device. '
                             'Defaults to VID:PID for AllPixel')
    parser.add_argument('--baud', default=921600, type=int,
                        help='Serial baud rate.')

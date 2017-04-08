from ..drivers.serial import DriverSerial, Devices, serial

CONNECT_MESSAGE = """
Connect just one Serial device (AllPixel) and press enter..."""

HELP = """Find serial devices."""


def run(args, settings):
    run = True
    print("Press Ctrl+C any time to exit.")
    try:
        while run:
            try:
                input(CONNECT_MESSAGE)
                devices = Devices()
                ports = devices.find_serial_devices()
                if not ports:
                    print("No serial devices found. Please connect one.")
                    continue

                port = sorted(ports.items())[0][1]
                id = devices.get_device_id(port)
                print("Device ID of {}: {}".format(port, id))
                newID = input("Input new ID (enter to skip): ")
                if newID != '':
                    try:
                        newID = int(newID)
                        if newID < 0 or newID > 255:
                            raise ValueError()

                        devices.set_device_id(port, newID)
                        id = devices.get_device_id(port)
                        print("Device ID set to: %s" % id)
                    except ValueError:
                        print("Please enter a number between 0 and 255.")
            except serial.SerialException as e:
                print("Problem connecting to serial device. %s" % e)

            except Exception as e:
                print('Programmer error with exception %s' % e)

    except KeyboardInterrupt:
        pass


def set_parser(parser):
    parser.set_defaults(run=run)

from __future__ import print_function
from ..drivers.serial import DriverSerial, Devices

CONNECT_MESSAGE = """
Connect just one Serial device (AllPixel) and press enter..."""

HELP = """Find serial devices."""


def run(args, settings):
    run = True
    print("Press Ctrl+C any time to exit.")
    try:
        while run:
            input(CONNECT_MESSAGE)
            devices = Devices()
            ports = devices.find_serial_devices()
            if len(ports):
                try:
                    id = devices.get_device_id(ports[0])
                    print("Device ID of {}: {}".format(ports[0], id))
                    newID = input("Input new ID (enter to skip): ")
                    if newID != '':
                        try:
                            newID = int(newID)
                            if newID < 0 or newID > 255:
                                raise ValueError()

                            try:
                                devices.set_device_id(ports[0], newID)
                                id = devices.get_device_id(ports[0])
                                print("Device ID set to: %s" % id)
                            except:
                                pass
                        except ValueError:
                            print("Please enter a number between 0 and 255.")
                except Exception as e:
                    print(e)
            else:
                print("No serial devices found. Please connect one.")

    except:
        pass


def set_parser(parser):
    parser.set_defaults(run=run)

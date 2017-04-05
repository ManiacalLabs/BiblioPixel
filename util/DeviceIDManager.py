from __future__ import print_function
from bibliopixel.drivers.serial import DriverSerial, DEVICES

CONNECT_MESSAGE = """
Connect just one Serial device (AllPixel) and press enter..."""


def run():
    run = True
    print("Press Ctrl+C any time to exit.")
    try:
        while run:
            ignored = input(CONNECT_MESSAGE)
            ports = DEVICES.findSerialDevices()
            if len(ports):
                try:
                    id = DEVICES.getDeviceID(ports[0])
                    print("Device ID of {}: {}".format(ports[0], id))
                    newID = input("Input new ID (enter to skip): ")
                    if newID != '':
                        try:
                            newID = int(newID)
                            if newID < 0 or newID > 255:
                                raise ValueError()

                            try:
                                DEVICES.setDeviceID(ports[0], newID)
                                id = DEVICES.getDeviceID(ports[0])
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


run()

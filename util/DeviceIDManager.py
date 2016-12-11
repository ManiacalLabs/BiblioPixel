from __future__ import print_function
import sys
from bibliopixel.drivers.serial_driver import DriverSerial

run = True
print("Press Ctrl+C any time to exit.")
try:
    while run:
        ignored = input("\nConnect just one Serial device (AllPixel) and press enter...")
        ports = DriverSerial.findSerialDevices()
        if len(ports):
            try:
                id = DriverSerial.getDeviceID(ports[0])
                print("Device ID of {}: {}".format(ports[0], id))
                newID = input("Input new ID (enter to skip): ")
                if newID != '':
                    try:
                        newID = int(newID)
                        if newID < 0 or newID > 255:
                            raise ValueError()

                        try:
                            DriverSerial.setDeviceID(ports[0], newID)
                            print("Device ID set to: {}".format(DriverSerial.getDeviceID(ports[0])))
                        except:
                            pass
                    except ValueError:
                        print("Please enter a valid number between 0 and 255.")
            except Exception as e:
                print(e)
        else:
            print("No serial devices found. Please connect one.")

except KeyboardInterrupt as err:
    pass
else:
    pass

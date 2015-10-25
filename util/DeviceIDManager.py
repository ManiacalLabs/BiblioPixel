import sys
from bibliopixel.drivers.serial_driver import *

run = True
print "Press Ctrl+C any time to exit."
try:
	while run:
		ignored = raw_input("\nConnect just one Serial device (AllPixel) and press enter...")
		ports = DriverSerial.findSerialDevices()
		if len(ports):
			try:
				id = DriverSerial.getDeviceID(ports[0])
				print "Device ID of {}: {}".format(ports[0], id)
				newID = raw_input("Input new ID (enter to skip): ")
				if newID != '':
					try:
						newID = int(newID)
						if newID < 0 or newID > 255:
							raise ValueError()

						try:
							DriverSerial.setDeviceID(ports[0], newID)
							print "Device ID set to: {}".format(DriverSerial.getDeviceID(ports[0]))
						except:
							pass
					except ValueError:
						print "Please enter a valid number between 0 and 255."
			except Exception, e:
				log.logger.error(e)
		else:
			print "No serial devices found. Please connect one."

except KeyboardInterrupt, err:
    pass
else:
    pass

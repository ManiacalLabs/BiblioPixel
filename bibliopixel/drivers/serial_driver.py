from driver_base import *
import sys
import time
import os
os.sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
import log
try:
    import serial, serial.tools.list_ports
except ImportError as e:
    error = "Please install pyserial 2.7+! pip install pyserial"
    log.logger.error(error)
    raise ImportError(error)

class BiblioSerialError(Exception):
    pass

class CMDTYPE:
    SETUP_DATA = 1 #config data (LED type, SPI speed, num LEDs)
    PIXEL_DATA = 2 #raw pixel data will be sent as [R1,G1,B1,R2,G2,B2,...]
    BRIGHTNESS = 3 #data will be single 0-255 brightness value, length must be 0x00,0x01
    GETID      = 4
    SETID      = 5

class RETURN_CODES:
    SUCCESS = 255 #All is well
    REBOOT = 42 #Device reboot needed after configuration
    ERROR = 0 #Generic error
    ERROR_SIZE = 1 #Data receieved does not match given command length
    ERROR_UNSUPPORTED = 2 #Unsupported command
    ERROR_PIXEL_COUNT = 3 #Too many pixels for device

class LEDTYPE:
    GENERIC = 0 #Use if the serial device only supports one chipset
    LPD8806 = 1
    WS2801  = 2
    #These are all the same
    WS2811 = 3
    WS2812 = 3
    WS2812B = 3
    NEOPIXEL = 3
    APA104 = 3
    #400khz variant of above
    WS2811_400 = 4

    TM1809 = 5
    TM1804 = 5
    TM1803 = 6
    UCS1903 = 7
    SM16716 = 8
    APA102 = 9
    LPD1886 = 10 
    P9813 = 11 

class DriverSerial(DriverBase):
    """Main driver for Serial based LED strips"""
    foundDevices = []
    deviceIDS = {}
    def __init__(self, type, num, dev="", c_order = ChannelOrder.RGB, SPISpeed = 2, gamma = None, restart_timeout = 3, deviceID = None, hardwareID = "1D50:60AB"):
        super(DriverSerial, self).__init__(num, c_order = c_order, gamma = gamma)

        if SPISpeed < 1 or SPISpeed > 24 or not (type == LEDTYPE.LPD8806 or type == LEDTYPE.WS2801 or type == LEDTYPE.SM16716):
            SPISpeed = 24

        self._hardwareID = hardwareID
        self._SPISpeed = SPISpeed
        self._com = None
        self._type = type
        self.dev = dev
        self.deviceID = deviceID
        if self.deviceID != None and (self.deviceID < 0 or self.deviceID > 255):
            raise ValueError("deviceID must be between 0 and 255")

        resp = self._connect()
        if resp == RETURN_CODES.REBOOT: #reboot needed
            log.logger.info("Reconfigure and reboot needed, waiting for controller to restart...")
            self._com.close()
            time.sleep(restart_timeout)
            resp = self._connect()
            if resp != RETURN_CODES.SUCCESS:
                DriverSerial._printError(resp)
            else:
                log.logger.info("Reconfigure success!")
        elif resp != RETURN_CODES.SUCCESS:
            DriverSerial._printError(resp)

    @staticmethod
    def findSerialDevices(hardwareID = "1D50:60AB"):
        if len(DriverSerial.foundDevices) == 0:
            DriverSerial.foundDevices = []
            DriverSerial.deviceIDS = {}
            for port in serial.tools.list_ports.grep(hardwareID):
                DriverSerial.foundDevices.append(port[0])
                id = DriverSerial.getDeviceID(port[0])
                DriverSerial.deviceIDS[id] = port[0]

        return DriverSerial.foundDevices

    @staticmethod
    def _printError(error):
        msg = "Unknown error occured."
        if error == RETURN_CODES.ERROR_SIZE:
            msg = "Data packet size incorrect."
        elif error == RETURN_CODES.ERROR_UNSUPPORTED:
            msg = "Unsupported configuration attempted."
        elif error == RETURN_CODES.ERROR_PIXEL_COUNT:
            msg = "Too many pixels specified for device."
        
        log.logger.error(msg)
        raise BiblioSerialError(msg)


    @staticmethod
    def _comError():
        error = "There was an unknown error communicating with the device."
        log.logger.error(error)
        raise IOError(error)

    def _connect(self):
        try:
            if(self.dev == ""):
                DriverSerial.findSerialDevices(self._hardwareID)

                if self.deviceID != None:
                    if self.deviceID in DriverSerial.deviceIDS:
                        self.dev = DriverSerial.deviceIDS[self.deviceID]
                        log.logger.info( "Using COM Port: {}, Device ID: {}".format(self.dev, self.deviceID))
                                
                    if self.dev == "":
                        error = "Unable to find device with ID: {}".format(self.deviceID)
                        log.logger.error(error)
                        raise ValueError(error)
                elif len(DriverSerial.foundDevices) > 0:
                    self.dev = DriverSerial.foundDevices[0]
                    devID = -1
                    for id in DriverSerial.deviceIDS:
                        if DriverSerial.deviceIDS[id] == self.dev:
                            devID = id

                    log.logger.info( "Using COM Port: {}, Device ID: {}".format(self.dev, devID))

            try:
                self._com =  serial.Serial(self.dev, timeout=5)
            except serial.SerialException as e:
                ports = DriverSerial.findSerialDevices(self._hardwareID)
                error = "Invalid port specified. No COM ports available."
                if len(ports) > 0:
                    error = "Invalid port specified. Try using one of: \n" + "\n".join(ports)
                log.logger.info(error)
                raise BiblioSerialError(error)
            
            packet = DriverSerial._generateHeader(CMDTYPE.SETUP_DATA, 4)
            packet.append(self._type) #set strip type
            packet.append(self.bufByteCount & 0xFF) #set 1st byte of byteCount
            packet.append(self.bufByteCount >> 8) #set 2nd byte of byteCount
            packet.append(self._SPISpeed)
            self._com.write(packet)

            resp = self._com.read(1)
            if len(resp) == 0:
                DriverSerial._comError()

            return ord(resp)

        except serial.SerialException as e:
            error = "Unable to connect to the device. Please check that it is connected and the correct port is selected."
            log.logger.exception(e)
            log.logger.error(error)
            raise e

    @staticmethod
    def _generateHeader(cmd, size):
        packet = bytearray()
        packet.append(cmd)
        packet.append(size & 0xFF)
        packet.append(size >> 8)
        return packet

    @staticmethod
    def setDeviceID(dev, id):
        if id < 0 or id > 255:
            raise ValueError("ID must be an unsigned byte!")

        try:
            com =  serial.Serial(dev, timeout=5)

            packet = DriverSerial._generateHeader(CMDTYPE.SETID, 1)
            packet.append(id)
            com.write(packet)

            resp = com.read(1)
            if len(resp) == 0:
                DriverSerial._comError()
            else:
                if ord(resp) != RETURN_CODES.SUCCESS:
                    DriverSerial._printError(ord(resp))

        except serial.SerialException as e:
            log.logger.error("Problem connecting to serial device.")
            raise IOError("Problem connecting to serial device.")
            

    @staticmethod
    def getDeviceID(dev):
        packet = DriverSerial._generateHeader(CMDTYPE.GETID, 0)
        try:
            com = serial.Serial(dev, timeout=5)
            com.write(packet)
            resp = ord(com.read(1))
            return resp
        except serial.SerialException as e:
            #log.logger.error("Problem connecting to serial device.")
            raise IOError("Problem connecting to serial device.")


    def setMasterBrightness(self, brightness):
        packet = DriverSerial._generateHeader(CMDTYPE.BRIGHTNESS, 1)
        packet.append(brightness)
        self._com.write(packet)
        resp = ord(self._com.read(1))
        if resp != RETURN_CODES.SUCCESS:
            DriverSerial._printError(resp)
            return False
        else:
            return True

    #Push new data to strand
    def update(self, data):
        count = self.bufByteCount
        packet = DriverSerial._generateHeader(CMDTYPE.PIXEL_DATA, count)

        c_order = self.c_order

        self._fixData(data)

        packet.extend(self._buf)
        self._com.write(packet)
        
        resp = self._com.read(1)
        if len(resp) == 0:
                DriverSerial._comError()
        if ord(resp) != RETURN_CODES.SUCCESS:
            DriverSerial._printError(ord(resp))

        self._com.flushInput()

        
        

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
    #400khz variant of above
    WS2811_400 = 4

    TM1809 = 5
    TM1804 = 5
    TM1803 = 6
    UCS1903 = 7
    SM16716 = 8

class DriverSerial(DriverBase):
    """Main driver for Serial based LED strips"""
    
    def __init__(self, type, num, dev="", c_order = ChannelOrder.RGB, SPISpeed = 16, gamma = None, restart_timeout = 3):
        super(DriverSerial, self).__init__(num, c_order = c_order, gamma = gamma)

        if SPISpeed < 1 or SPISpeed > 24 or not (type == LEDTYPE.LPD8806 or type == LEDTYPE.WS2801 or type == LEDTYPE.SM16716):
            SPISpeed = 24

        self._SPISpeed = SPISpeed
        self._com = None
        self._type = type
        self.dev = dev

        resp = self._connect()
        if resp == RETURN_CODES.REBOOT: #reboot needed
            log.logger.info("Reconfigure and reboot needed, waiting for controller to restart...")
            self._com.close()
            time.sleep(restart_timeout)
            resp = self._connect()
            if resp != RETURN_CODES.SUCCESS:
                self._printError(resp)
            else:
                log.logger.info("Reconfigure success!")
        elif resp != RETURN_CODES.SUCCESS:
            self._printError(resp)


    def _printError(self, error):
        msg = "Unknown error occured."
        if error == RETURN_CODES.ERROR_SIZE:
            msg = "Data packet size incorrect."
        elif error == RETURN_CODES.ERROR_UNSUPPORTED:
            msg = "Unsupported configuration attempted."
        elif error == RETURN_CODES.ERROR_PIXEL_COUNT:
            msg = "Too many pixels specified for device."
        
        log.logger.error(msg)
        raise BiblioSerialError(msg)


    def _comError(self):
        error = "There was an unknown error communicating with the device."
        log.logger.error(error)
        raise IOError(error)

    def _connect(self):
        try:
            if(self.dev == ""):
                com_list = serial.tools.list_ports.grep("4242:8037")
                try:
                    port = com_list.next()
                    self.dev = port[0]
                    log.logger.info( "Using COM Port: {:}".format(self.dev))
                except StopIteration:
                    pass

            try:
                self._com =  serial.Serial(self.dev, timeout=5)
            except serial.SerialException as e:
                ports = list(serial.tools.list_ports.comports())
                error = "Invalid port specified. No COM ports available."
                if len(ports) > 0: 
                    p_list = []
                    for p in ports:
                        p_list.append(p[0] + " - " + p[1])

                    error = "Invalid port specified. Try using one of: \n" + "\n".join(p_list)
                log.logger.info(error)
                raise BiblioSerialError(error)
            
            packet = self._generateHeader(CMDTYPE.SETUP_DATA, 4)
            packet.append(self._type) #set strip type
            packet.append(self.bufByteCount & 0xFF) #set 1st byte of byteCount
            packet.append(self.bufByteCount >> 8) #set 2nd byte of byteCount
            packet.append(self._SPISpeed)
            self._com.write(packet)

            resp = self._com.read(1)
            if len(resp) == 0:
                self._comError()

            return ord(resp)

        except serial.SerialException as e:
            error = "Unable to connect to the device. Please check that it is connected and the correct port is selected."
            log.logger.exception(e)
            log.logger.error(error)
            raise e

    def _generateHeader(self, cmd, size):
        packet = bytearray()
        packet.append(cmd)
        packet.append(size & 0xFF)
        packet.append(size >> 8)
        return packet

    def setMasterBrightness(self, brightness):
        packet = self._generateHeader(CMDTYPE.BRIGHTNESS, 1)
        packet.append(brightness)
        self._com.write(packet)
        resp = ord(self._com.read(1))
        if resp != RETURN_CODES.SUCCESS:
            self._printError(resp)
            return False
        else:
            return True

    #Push new data to strand
    def update(self, data):
        count = self.bufByteCount
        packet = self._generateHeader(CMDTYPE.PIXEL_DATA, count)

        c_order = self.c_order

        self._fixData(data)

        packet.extend(self._buf)
        self._com.write(packet)
        
        resp = self._com.read(1)
        if len(resp) == 0:
                self._comError()
        if ord(resp) != RETURN_CODES.SUCCESS:
            self._printError(ord(resp))

        self._com.flushInput()

        
        

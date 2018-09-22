import unittest
from unittest import mock
from bibliopixel.drivers.return_codes import RETURN_CODES
from bibliopixel.drivers.serial import driver
from test.bibliopixel.drivers.dummy_test import clock_only_project


class DriverTest(unittest.TestCase):
    @mock.patch('serial.Serial', autospec=True)
    @mock.patch('bibliopixel.drivers.serial.driver.Devices', autospec=True)
    def test_driver(self, Devices, Serial):
        device_id, port, version = 10, 23, 5
        dev, device_version = '/dev/wombat', 0
        device_map = {device_id: (port, version)}

        instance = Devices.return_value
        instance.find_serial_devices.return_value = device_map
        instance.get_device.return_value = device_id, dev, device_version
        instance.baudrate = 921600

        instance = Serial.return_value
        instance.read.return_value = chr(RETURN_CODES.SUCCESS)

        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        sd = driver.Serial(ledtype=0, num=len(colors))
        sd.set_project(clock_only_project())
        sd.set_colors(colors, 0)
        sd.start()
        sd.update_colors()
        sd.sync()
        sd.cleanup()

        def call_write(*args):
            return mock.call().write(bytearray(args))

        expected = [
            mock.call().find_serial_devices(),
            mock.call().get_device(None)]
        self.assertEqual(Devices.method_calls, expected)

        expected = [
            call_write(1, 4, 0, 0, 9, 0, 1),
            mock.call().read(1),
            call_write(2, 9, 0, 255, 0, 0, 0, 255, 0, 0, 0, 255),
            mock.call().read(1),
            mock.call().flushInput(),
            mock.call().close()]

        self.assertEqual(Serial.method_calls, expected)

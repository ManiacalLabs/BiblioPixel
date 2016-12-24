import pytest
import pytest_benchmark

from bibliopixel.drivers.driver_base import DriverBase
from bibliopixel import LEDStrip


PIXEL_COUNT = 1000


@pytest.fixture(scope="module")
def led():
    driver = DriverBase(num=PIXEL_COUNT)
    return LEDStrip(driver)


def test_fill(led, benchmark):
    def do_fill(led):
        for i in range(256):
            led.fill((i, i, i))
            led.update()
    benchmark(do_fill, led)


def test_fill_hsv(led, benchmark):
    def do_fill_hsv(led):
        for i in range(256):
            led.fillHSV((i, 255, 255))
            led.update()
    benchmark(do_fill_hsv, led)

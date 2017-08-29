from . base import TypesBaseTest
from bibliopixel.drivers.SPI.interfaces import SPI_INTERFACES


class SpiInterfaceTypesTest(TypesBaseTest):
    def test_some(self):
        self.make('spi_interface', 'FILE')
        self.make('spi_interface', 'DUMMY')
        self.make('spi_interface', SPI_INTERFACES.PYDEV)

        with self.assertRaises(ValueError):
            self.make('spi_interface', 7)

        with self.assertRaises(KeyError):
            self.make('spi_interface', 'NONE')

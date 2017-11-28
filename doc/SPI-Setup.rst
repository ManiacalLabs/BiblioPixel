SPI Setup
=========

***The following section is only valid for embedded devices that have
hardware SPI ports, such as the Raspberry Pi and Beagle Bone Black. SPI
usage should be possible on other devices, but will not be covered in
this documentation. If you have tested and confirmed SPI usage on
another device please log an issue ticket with exact details and they
will be added to this documentation.***

Requirements
------------

While SPI drivers (those inheriting from [[DriverSPIBase]]) can
interface with SPI via file access methods, doing so is much slower than
direct access. For optimal performance, install
`py-spidev <https://github.com/doceme/py-spidev>`__:

::

    pip install spidev

Voltage Protection
------------------

While not *absolutely* necessary, it is highly recommended to use a
`level shifter <http://www.adafruit.com/products/757>`__. This is
because the Raspberry Pi & BeagleBone Black use 3.3V logic and most LED
strips use 5V. Since only the SPI output is being used it should not
harm the strip or the Pi but the logic voltage may be too low for the
strip, especially over long distances. ## Raspberry Pi

It is recommended to use Raspbian when access to the SPI port is needed.
To enable SPI usage, log into the Pi console and run:

::

    sudo nano /etc/modprobe.d/raspi-blacklist.conf

The change the line:

::

    blacklist spi-bcm2708

to

::

    #blacklist spi-bcm2708

This will remove the blacklisting from the SPI device and allow the
driver to load on boot. Reboot the device with:

::

    sudo shutdown -r now

You can also enable SPI using the
`raspi-config <http://www.raspberrypi.org/documentation/configuration/raspi-config.md>`__
utility.

Once SPI has been enabled, your LED strip should be connected to the PI
like in the image below:

[[img/RPi\_LEDStrip\_bb.png]][Click for larger
view](img/RPi\_LEDStrip\_bb.png)

On the new model Pi boards it has a 40 pin header instead of 32, but the
pin numbers require are the same. 19 (MOSI) for Data and 23 (SCLK) for
Clock. See the pinouts below to help find the pins you need:

Pi A & B:
'''''''''

[[img/Pi1Header.png]]

Pi A+, B+, & 2:
'''''''''''''''

[[img/Pi2Header.png]]

Beagle Bone Black
-----------------

The BBB has two SPI ports, SPI0 and SPI1. Since SPI1 is not usable at
the same time as HDMI, we will only cover setup of SPI0. The official
documentation for enabling SPI is here:
http://elinux.org/BeagleBone\_Black\_Enable\_SPIDEV#SPI0 Unfortunately,
it seems to be outdated and has never worked for us. As long as you are
using the latest Debian image, the below should work for you.

Load uEnv.txt either by plugging the BBB into your computer via USB or
via:

::

    sudo nano /boot/uboot/uEnv.txt

Paste the following line at the end of the file:

::

    optargs=quiet drm.debug=7 capemgr.enable_partno=BB-SPIDEV0

Save the file and reboot your beaglebone black:

::

    sudo reboot

Make sure it is enabled:

::

    ls -al /dev/spidev*

You should see the following:

::

    crw-rw---T 1 root spi 153, 1 May 15 02:22 /dev/spidev1.0
    crw-rw---T 1 root spi 153, 0 May 15 02:22 /dev/spidev1.1

Note: By using the pre-compiled overlay that comes on the device, the
SPI port is in fact named spidev1.\* instead of spidev0.\* This is
*still* the SPI0 device, despite the file name.

You should also be able to see the pingroups:

::

    cat /sys/kernel/debug/pinctrl/44e10800.pinmux/pingroups

The output will contain:

::

    group: pinmux_bb_spi0_pins
    pin 84 (44e10950)
    pin 85 (44e10954)
    pin 86 (44e10958)
    pin 87 (44e1095c)

So, as you see, it is still using SPI0.

Note: The SPI port you want to use for the below pins is /dev/spidev1.0

Once SPI has been enabled, your LED strip should be connected to the BBB
like in the image below:

[[img/BBB\_LEDStrip\_bb.png]][Click for larger
view](img/BBB\_LEDStrip\_bb.png)

*Note*: PiWS281X is for the Raspberry Pi only and has not been tested on
any other platform!

Installation
------------

PiWS281X requires the installation of the
`rpi\_ws281x <https://github.com/jgarff/rpi_ws281x>`__ library which
includes a C module and Python wrapper. There is currently no pip
install available, but it can be installed with a few commands.

::

    git clone https://github.com/jgarff/rpi_ws281x.git
    cd rpi_ws281x
    sudo apt-get install python-dev swig scons
    sudo scons
    cd python
    sudo python setup.py build install

At this point, rpi\_ws281x should be importable from python as
``neopixel`` and you will be ready to use PiWS281X

## v3.4.1 - 2018-01-04
- Fix broken PiWS281X
- Fix `bp demo`

## v3.4.0 - 2017-12-29
- default settings for projects
- saved defaults
- better numpy integration and new "numbers" project section
- new "slideshow" mode for sequences
- per project aliases and many improvements and bugfixes to aliases
- bp can now run .py files
- Debug logging is streamlined
- Animations can now set their own default projects
- Many more

## v3.3.6 - 2017-11-24
- Fixed #485 even yet more

## v3.3.5 - 2017-11-24
- Fixed #485 somewhat more

## v3.3.4 - 2017-11-23
- Fixed #485, #471, network brightness, and ring_rotation

## v3.3.1 - 2017-08-23
- Added auto_demo for remote UI
- Bug fixes

## v3.3.0 - 2017-09-19
- Overhauled multi-driver coord_map system

## v3.2.0 -	2017-08-13
- Remote UI triggers
- Other bug fixes

## v3.1.0 - 2017-07-23
- New remote UI
- Many bug fixes and usability tweaks

## v3.0.3 - 2017-06-23

BiblioPixel v3.0 is a nearly complete rewrite making it stronger, better, faster, and with many new amazing features.

- Completely Python 3 compatible
- Faster frame generation and hardware updates
- Brand-new [SimPixel](https://github.com/ManiacalLabs/SimPixel) visualizer uses WebGL to visualize lighting designs in the browser!
- Better matrix text handling
- Better matrix and cube layout building
- BiblioPixel Projects - blinkin' lights with only a simple config, no code!
- Built-in demos
- Greatly improved base LED types along with new Circle and Cube
- Overhauled SPI driver support
- Support for WS2812 (NeoPixel) on the Raspberry Pi and similar
- Many more!

### v2.0.10
- Support py-spidev 3.x series

### v2.0.7
- Fixed LEDPOV driver crash
- Cleanup / Reformat of all code

### v2.0.6
- Fix Issue #28: Error parsing new pyserial version

### v2.0.5
- Fixes to LEDCircle

### v2.0.3
- Fixed clear before run bug

### v2.0.2
- Fixed Spelling
- Fixed untilComplete/max_steps bug

### v2.0.0
- Added BaseGameAnim
- Added GamePad controls
- Added AnimationQueue
- Added "with" construct support
- Added Texture maps
- Added controller level masterBrightness
- Added transparency support
- Added Manifests for PixelWeb

- New, smaller font
- Moved built in animations to BiblioPixelAnimations
- Improved Image file manipulation
- Better threading

- Many speed improvements
- Many, many bug fixes

### v1.2.4
Adding util.py to support BiblioPixelAnimations

### v1.2.3
Fixing APA102 driver

### v1.2.2
- Improved LEDCircle Rendering
- Various bug fixes

### v1.2.1
Added DriverAPA102

### v1.2.0
- Added LEDPOV, LEDCircle Classes
- Added Serial Device Version Support
- Improved Serial Device detection
- Added threaded animation support

### v1.1.7
- Added check for pyserial version
- Forced case insenitive grep for USB ID

### v1.1.6
Bug fix for APA102 support in DriverSerial

### v1.1.5
Bug fixes for AllPixel support

### v1.1.4
Removed debug print statements

### v1.1.3
Fixed bug with LEDMatrix setRGB/setHSV

### v1.1.1
bug fixes
added Philips Hue driver

### v1.1.0
- Multi-device support
- Device ID Support
- Various bug fixes

### v1.0.0
- Initial release

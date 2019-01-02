## v3.4.42 - 2019-01-03
- Fix `bp devices`
- Better shutdown for Builder
- Fix animation.fill.Fill

## v3.4.41 - 2018-12-02
- Fix issue with classic projects where run.seconds != 0
- Better release tests

## v3.4.40 - 2018-11-30
- Fix #1094, #1088, #1084, #1076 and probably #1085
- Make all Yaml dumping safe

## v3.4.39 - 2018-11-26
- New Project Builder class
- Make Color class more user-friendly
- Improvements to error reporting in scripts

## v3.4.38 - 2018-11-21
- Fix MANIFEST for templates used by `bp new`
- New user colors

## v3.4.37 - 2018-11-21
- Initialize self._step in animation.Animation

## v3.4.36 - 2018-11-20
- Stop using deprecated features
- Better help
- Clean up directory structure

## v3.4.35 - 2018-11-19
- Make scripts/new_version more Windows-compatible

## v3.4.34 - 2018-11-19
- Fix setup.py for Windows

## v3.4.33 - 2018-11-18
- Better GIF file generation

## v3.4.32 - 2018-11-18
- Fix demos (#1048, #1049)
- Load commands individually for faster startup (#10433)

## v3.4.31 - 2018-11-15
- Fix issues #978, #984, #988, #991, #1023, #1025, #1040, #1042, #1043
- New default palettes
- Much smoother animations in many cases
- More documentation
- Improvements to `bp info`

## v3.4.30 - 2018-10-23
- Revert change that broken LarsonScanners, affected others
- New mp4 extractor
- Bigger default GIF sizes (fix #1019)

## v3.4.29 - 2018-10-16
- Better legacy palettes

## v3.4.28 - 2018-10-14
- Legacy palettes allow BPA animations to easily use palettes

## v3.4.27 - 2018-10-13
- Better palettes

## v3.4.26 - 2018-10-13
- Much more documentation
- Better extracted GIFs
- New Palette.autoscale feature

## v3.4.25 - 2018-10-04
- Bump version number

## v3.4.24 - 2018-10-04
- Bump version number

## v3.4.23 - 2018-10-04
- New color palette class
- Simplify entering channel order in Projects
- Fix intermittent timer issue

## v3.4.22 - 2018-10-02
- Fix #991

## v3.4.21 - 2018-10-02
- Include main/commands.rst.tmpl (fix #988)

## v3.4.20 - 2018-09-24
- Fixes for classic "no project" BP
- Get rid of deprecation warnings from new version of pytest

## v3.4.19 - 2018-07-23
- Support Python 3.7
- New `bp-pid` command
- New `curses` and `text` drivers display LED colors in a terminal
- New `release_test` integration test suite with hardware tests
- Switch to using YAML as default data storage
- Fix or implement #663, #720, #725, #786, #787, #788, #792, #793,
  #795,  #796, #802, #813, #819, #827, #836, #861, #863, #863, #870, #872,
  #874, #876, #878, #885, #892, #898, #910, #925, #927, #929 and #938
- Much more...

## v3.4.18 - 2018-05-04
- Remove test that crashes ArtNet
- Test project for ArtNet

## v3.4.17 - 2018-05-03
- Rework Runnable and threads for better shutdown
- New ArtNet control

## v3.4.16 - 2018-04-19
- Better error handling
- Add a timeout to UDP sockets
- Better handling of partial colors and component color lists

## v3.4.15 - 2018-04-11
- New `bp restart` and `bp shutdown` commands replace `bp signal`
- layout.Matrix now stores parameters needed for cloning
- Better error message in QueuedAddress
- Make all project keys strings (fix #752)

## v3.4.14 - 2018-04-08
- Add RemoteServer.shutdown_server() classmethod and SIGHUP fix
- Always exit from main using sys.exit()

## v3.4.13 - 2018-04-08
- Re-read project files on SIGHUP
- Better signal handling (SIGHUP, SIGINT, SIGETERM)
- Fix `bp run --dump` option
- Give a better warning if Layout.start() is not called

## v3.4.12 - 2018-04-05
- Remove print statement

## v3.4.11 - 2018-04-04
- Restart `bp` on SIGHUP (fix #724)
- Command line flags override project files (fix #694)
- Use recursive name-guessing (fix #652)
- Compute animation.name in Animation.pre_recursion (fix #722 and #723)

## v3.4.10 - 2018-03-31
- Fix PiWS281X.set_brightness (fix #715)
- Allow controls to raise exceptions (fix #711)
- Allow animations to be retrieved by name
- Better error messages

## v3.4.9 - 2018-03-28
- Add numpy to requirements
- Fix `bp demo circle`
- Make layout.color_list setter more flexible
- Refactorings

## v3.4.8 - 2018-03-26
- Fix #686 and #689
- Allow animation.Remote to open the URL for its control page
- --v4 flag

## v3.4.7 - 2018-03-19
- Adding preliminary ArtNet support
- Better error reporting
- More documentation
- Fine-grained steps in Sequence
- More work on general controls
- UDP framework
- Project event queue
- Fixed Serial brightness

## v3.4.6 - 2018-02-10
- Fix crash in `bp demo`

## v3.4.5 - 2018-02-09
- Add fail parameter to serial.Devices.error
- Lots of documentation

## v3.4.4 - 2018-02-01
- Split splits a Strip to run multiple animations at once
- Make float32 the default float type
- Report if we aren't using sudo for PiWS281X driver (fix #582)
- scripts/new_version

## v3.4.3 - 2018-01-26
- Fix log.info
- Much more information from `bp --help`

## v3.4.2 - 2018-01-12
- Fix SPI Driver

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

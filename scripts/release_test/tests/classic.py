#!/usr/bin/env python3


def main():
    import bibliopixel
    from bibliopixel.drivers import simpixel

    bibliopixel.log.setLogLevel(bibliopixel.log.DEBUG)

    # set number of pixels & LED type here
    driver = simpixel.SimPixel(num=32)

    # load the LEDStrip class
    from bibliopixel.layout import Strip
    led = Strip(driver)

    # load channel test animation
    from bibliopixel.animation import StripChannelTest
    anim = StripChannelTest(led)
    driver.open_browser()

    try:
        # run the animation
        anim.run(seconds=4)

    finally:
        # Ctrl+C will exit the animation and turn the LEDs offs
        led.all_off()
        led.update()


def run():
    import common
    common.test_prompt('classic')
    common.execute('python', __file__)


if __name__ == '__main__':
    main()

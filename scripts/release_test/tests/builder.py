import os, tempfile, threading, time
import common
from bibliopixel.builder import Builder
from bibliopixel.animation.tests import StripChannelTest
from bibliopixel.drivers.simpixel import SimPixel

SAVE_FILE = 'save.yml'


def run():
    common.test_prompt('builder')

    with tempfile.TemporaryDirectory() as td:
        save_file = os.path.join(td, SAVE_FILE)
        pb = Builder()
        desc = pb.desc
        desc.shape = 32
        desc.animation = '.tests.PixelTester'
        pb.simpixel()

        def stop():
            time.sleep(2)
            pb.stop()

        def start_and_stop():
            threading.Thread(daemon=True, target=stop).start()
            pb.start()

        start_and_stop()

        pb.save(save_file)
        pb.clear()

        pb = Builder(save_file)
        start_and_stop()

        pb.danimation = StripChannelTest
        start_and_stop()

        pb.animation = '$bpa.strip.Wave'
        pb.threaded = True
        pb.start()
        time.sleep(2)
        pb.project.animation.palette[0] = 'green'
        pb.stop()
        pb = None

        # TODO: why do we only have to do this for this one test?
        SimPixel.close_all()

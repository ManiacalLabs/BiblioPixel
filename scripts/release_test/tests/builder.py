import os, tempfile, threading, time
import common
from bibliopixel.project.builder import Builder
from bibliopixel.animation.tests import StripChannelTest

SAVE_FILE = 'save.yml'


def run():
    common.prompt('Press return to start builder test')

    with tempfile.TemporaryDirectory() as td:
        save_file = os.path.join(td, SAVE_FILE)
        pb = Builder()
        pb.shape = 32
        pb.animation = '.tests.PixelTester'
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

        pb.animation = StripChannelTest
        start_and_stop()

        pb.animation = '$bpa.strip.Wave'
        pb.threaded = True
        pb.start()
        time.sleep(2)
        pb.project.animation.palette[0] = 'green'
        stop()

import threading, time
from .. import log


class AnimationThreading(object):
    """
    AnimationThreading handles threading - and eventually multiprocessing - for
    BaseAnimation.
    """

    def __init__(self, animation):
        self.animation = animation
        self.animation_stop_event = threading.Event()
        self.animation_thread = None

    def report_framerate(self, start, mid, now):
        stepTime = int(mid - start)
        render_duration = int(now - mid)
        totalTime = stepTime + render_duration
        fps = int(1000.0 / max(totalTime, 1))
        log.debug("%sms/%sfps / Frame: %sms / Update: %sms",
                  totalTime, fps, stepTime, render_duration)

    def stop_animation_thread(self, wait=False):
        if self.animation_thread:
            self.animation_stop_event.set()

            if wait:
                self.animation_thread.join()

    def animation_stopped(self):
        return not (self.animation_thread and self.animation_thread.isAlive())

    def animation_wait(self, t):
        if self.use_animation_thread:
            self.animation_stop_event.wait(t)
        else:
            time.sleep(t)

    def run_animation(self, run, threaded, join_thread):
        self.use_animation_thread = threaded
        if self.use_animation_thread:
            self.animation_stop_event.clear()

            def target():
                # TODO: no testpath exercises this code...
                log.debug('Starting thread...')
                run()
                log.debug('Thread Complete')

            self.animation_thread = threading.Thread(target=target, daemon=True)
            self.animation_thread.start()
            if join_thread:
                self.animation_thread.join()
        else:
            run()

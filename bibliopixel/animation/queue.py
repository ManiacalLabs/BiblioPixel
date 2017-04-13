from . base import BaseAnimation


class AnimationQueue(BaseAnimation):

    def __init__(self, led, anims=None):
        super().__init__(led)
        self.anims = anims or []
        self.curAnim = None
        self.animIndex = 0
        self._internalDelay = 0  # never wait
        self.fps = None
        self.until_complete = False

    # overriding to handle all the animations
    def stopThread(self, wait=False):
        for a, r in self.anims:
            # a bit of a hack. they aren't threaded, but stops them anyway
            a.thread_strategy.stop_event.set()
        self.thread_strategy.stop_thread(wait)

    def addAnim(self, anim, amt=1, fps=None, max_steps=0, until_complete=False,
                max_cycles=0, seconds=None):
        a = (
            anim,
            {
                "amt": amt,
                "fps": fps,
                "max_steps": max_steps,
                "until_complete": until_complete,
                "max_cycles": max_cycles,
                "seconds": seconds
            }
        )
        self.anims.append(a)

    def preRun(self, amt=1):
        self.animIndex = -1

    def run(self, amt=1, fps=None, sleep_time=0, max_steps=0, until_complete=False,
            max_cycles=0, threaded=False, join_thread=False, seconds=None):
        self.fps = fps
        self.until_complete = until_complete
        super().set_run(amt=1, fps=None, sleep_time=0, max_steps=0,
                        until_complete=until_complete,
                        max_cycles=0, seconds=seconds)
        super().run(threaded=threaded, join_thread=join_thread)

    def step(self, amt=1):
        self.animIndex += 1
        if self.animIndex >= len(self.anims):
            if self.until_complete:
                self.animComplete = True
            else:
                self.animIndex = 0

        if not self.animComplete and self.anims:
            self.curAnim = self.anims[self.animIndex]

            anim, run = self.curAnim
            run.update(threaded=False, join_thread=False)

            run['fps'] = run.get('fps') or self.fps
            anim.run(**(run))

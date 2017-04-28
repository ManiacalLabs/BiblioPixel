from . animation import BaseAnimation


class Sequence(BaseAnimation):
    IS_SEQUENCE = True

    def __init__(self, led, animations=None):
        super().__init__(led)
        self.animations = animations or []
        self.current_animation = None
        self.index = 0
        self.internal_delay = 0  # never wait

    # overriding to handle all the animations
    def stopThread(self, wait=False):
        for a, r in self.animations:
            # a bit of a hack. they aren't threaded, but stops them anyway
            a.thread_strategy.stop_event.set()
        self.thread_strategy.stop_thread(wait)

    def add_animation(self, anim, amt=1, fps=None, max_steps=0,
                      until_complete=False, max_cycles=0, seconds=None):
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
        self.animations.append(a)

    def preRun(self, amt=1):
        self.index = -1

    def step(self, amt=1):
        self.index += 1
        if self.index >= len(self.animations):
            if self.runner.until_complete:
                self.completed = True
            else:
                self.index = 0

        if not self.completed and self.animations:
            self.current_animation = self.animations[self.index]

            anim, run = self.current_animation
            run.update(threaded=False, join_thread=False)

            run['fps'] = run.get('fps') or self.runner.fps
            anim.run(**run)

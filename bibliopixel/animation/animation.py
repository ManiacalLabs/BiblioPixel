import contextlib, threading, time
from . import adaptor
from . runner import Runner, STATE
from .. util import deprecated, log
from .. util.threads.animation_threading import AnimationThreading
from .. project import attributes, fields


class Animation(object):
    free_run = False
    pre_recursion = fields.default_converter
    FAIL_ON_EXCEPTION = False

    @classmethod
    def construct(cls, project, *, run=None, name=None, data=None, **desc):
        """
        Construct an animation, set the runner, and add in the two
        "reserved fields" `name` and `data`.
        """
        from . failed import Failed
        exception = desc.pop('_exception', None)
        if exception:
            a = Failed(project.layout, desc, exception)
        else:
            try:
                a = cls(project.layout, **desc)
                a._set_runner(run or {})
            except Exception as e:
                if cls.FAIL_ON_EXCEPTION:
                    raise
                a = Failed(project.layout, desc, e)

        a.name = name
        a.data = data
        return a

    def __init__(self, layout, *, preclear=True, **kwds):
        attributes.set_reserved(self, 'animation', **kwds)
        self.layout = layout
        self.internal_delay = None
        self.on_completion = None
        self.state = STATE.ready
        self.preclear = preclear
        self.project = None
        self.runner = None
        self.time = time.time

    def set_project(self, project):
        self.project = project
        self.time = project.time
        if self.runner:
            self.runner.set_project(project)
            self.threading.set_project(project)

    @property
    def _led(self):
        """Many BiblioPixelAnimations use the "protected" variable _led."""
        return self.layout

    @_led.setter
    def _led(self, layout):
        self.layout = layout

    @property
    def color_list(self):
        return self.layout.color_list

    @color_list.setter
    def color_list(self, cl):
        self.layout.color_list = cl

    @property
    def completed(self):
        """Many BiblioPixelAnimations use the old `completed` variable."""
        return self.state == STATE.complete

    @completed.setter
    def completed(self, state):
        self.state = STATE.complete if state else STATE.running

    def pre_run(self):
        pass

    @property
    def title(self):
        return self.__class__.__name__

    def step(self, amt=1):
        pass

    def cleanup(self, clean_layout=True):
        self.threading.cleanup()
        # Some cases we may not want to clear the screen
        # Like with the remote, it would flash between anims
        if clean_layout:
            self.layout.cleanup()

    def preframe_callback(self):
        """
        preframe_callback is called right before the start of a frame rendering
        pass.

        The ``Project`` writes over this method, for the top-level animation
        only, in order to drain its edit_queue at a moment where no rendering
        is happening to avoid race conditions.
        """
        pass

    def start(self):
        self.threading.start()

    def stop(self):
        self.threading.stop_event.set()

    def join(self, timeout=None):
        self.threading.join(timeout)

    def run_all_frames(self):
        for i in self.generate_frames():
            pass

    def generate_frames(self, clean_layout=True):
        self._pre_run()
        try:
            if self.runner.repeats != 0:
                while self.state == STATE.running:
                    self._run_one_frame()
                    yield
        finally:
            self.cleanup(clean_layout)

        self.on_completion and self.on_completion(self.state)
        self.state = STATE.ready

    def _check_delay(self):
        if self.free_run:
            self.sleep_time = None
        elif self.internal_delay:
            self.sleep_time = self.internal_delay
        else:
            self.sleep_time = self.runner.sleep_time
        self.layout.animation_sleep_time = self.sleep_time or 0

    def _run_one_frame(self):
        timestamps = [self.time()]

        self.preframe_callback()
        timestamps = [self.time()]

        self.step(self.runner.amt)
        timestamps.append(self.time())

        self.layout.frame_render_time = timestamps[1] - timestamps[0]
        self.layout.push_to_driver()

        timestamps.append(self.time())
        _report_framerate(timestamps)

        self.cur_step += 1
        if self.state == STATE.complete and self.runner.max_cycles > 0:
            if self.cycle_count < self.runner.max_cycles - 1:
                self.cycle_count += 1
                self.state = STATE.running

        self.threading.wait(self.sleep_time, timestamps)
        if self.threading.stop_event.isSet():
            self.state = STATE.canceled
        else:
            self.state = self.runner.compute_state(self.cur_step, self.state)

    def _pre_run(self):
        self.state = STATE.running
        self.runner.run_start_time = self.time()
        self.threading.stop_event.clear()

        self.cur_step = 0
        self.cycle_count = 0

        self._check_delay()
        adaptor.adapt_animation_layout(self)
        self.preclear and self.layout.all_off()

        self.pre_run()

    def _set_runner(self, runner):
        self.runner = Runner(**(runner or {}))
        self.threading = AnimationThreading(self.runner, self.run_all_frames)
        if self.project:
            self.runner.set_project(self.project)
            self.threading.set_project(self.project)

    # DEPRECATED
    @property
    def _step(self):
        return self.cur_step

    @_step.setter
    def _step(self, step):
        self.cur_step = step

    def run(self, **kwds):
        deprecated.deprecated('BaseAnimation.run')
        self._set_runner(kwds)
        self.layout.start()
        self.start()


if deprecated.allowed():  # pragma: no cover
    BaseAnimation = Animation


def _report_framerate(timestamps):
    total_time = timestamps[-1] - timestamps[0]
    fps = int(1.0 / max(total_time, 0.001))
    log.frame("%dms/%dfps / Frame: %dms / Update: %dms",
              1000 * total_time,
              fps,
              1000 * (timestamps[1] - timestamps[0]),
              1000 * (timestamps[2] - timestamps[1]))

import os, time
from . import file_writer, renderer
from .. import colors, log

DEFAULT_RENDER = {
    'color': colors.Black,
    'pixel_width': 12,
    'pixel_height': None,
    'ellipse': True,
    'vertical': False,
    'frame': 2,
    'padding': 2,
}


class MovieWriter:
    """Write an animated GIF given frames from an animation."""

    def __init__(self, filename='output.gif', render=None,
                 divide=1, frames=128, time=10, speed=1.0, options=None,
                 gif_dir=None, duration=None, fps=None):
        self.render = dict(DEFAULT_RENDER, **(render or {}))
        self.divide = divide
        self.frames = frames
        self.time = time
        self.speed = speed
        self.duration = duration
        self.fps = fps
        self.options = options or {}
        self.gif_dir = gif_dir

        filename = os.path.expanduser(os.path.abspath(filename))
        file_root, suffix = os.path.splitext(filename)
        self.suffix = suffix

        self.filename = file_root + suffix
        self.basename = os.path.basename(file_root)
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)

        self.finished = False
        self.stop_after_write = True
        self.times = []

    def set_project(self, project):
        self.project = project
        self.render = renderer.renderer(project.layout, **self.render)
        assert self.render
        self.file_writer = file_writer.file_writer(self)
        self.fps = project.animation.runner.fps

    def step(self, cur_step):
        if self.finished or (self.divide >= 1 and cur_step % self.divide):
            return True

        self.frame = cur_step / max(self.divide, 1)
        self.times.append(self.project.time())

        if self.time:
            elapsed = self.times[-1] - self.times[0]
            self.finished = (elapsed >= self.time)
        else:
            self.finished = (self.frame >= self.frames)

        if self.finished:
            self.write()
        else:
            self.file_writer.step()

        return self.finished

    def write(self):
        self.file_writer.write()

    @property
    def length(self):
        return self.times and self.times[-1] - self.times[0] or 0

    @property
    def fps(self):
        if self._fps:
            return self._fps

        if self.duration:
            return 1 / self.duration

        if len(self.times) < 2:
            return 1

        return (len(self.times) - 1) / self.length

    @fps.setter
    def fps(self, fps):
        self._fps = fps

    @property
    def scaled_fps(self):
        return self.fps * self.speed

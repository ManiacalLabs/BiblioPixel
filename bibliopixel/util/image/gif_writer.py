import os, shutil, statistics, tempfile, time, traceback
from . import gif, mp4, renderer
from .. import colors, log


DEFAULT_RENDER = {
    'color': colors.Black,
    'pixel_width': 2,
    'pixel_height': None,
    'ellipse': True,
    'vertical': False,
    'frame': 3,
    'padding': 1,
}

WRITERS = {
    '.gif': gif.write_gif,
    '.mp4': mp4.write,
}


class GifWriter:
    """Write an animated GIF given frames from an animation."""

    def __init__(self, filename='gif_writer', render=None,
                 divide=1, frames=128, time=10, speed=1.0, gif_options=None,
                 tmp_dir=None, remove_tmp_dir=False, suffix='.gif',
                 duration=None, fps=None):
        self.render = dict(DEFAULT_RENDER, **(render or {}))
        self.divide = divide
        self.frames = frames
        self.time = time
        self.frame_files = []
        self.speed = speed
        self.duration = duration
        self.fps = fps
        self.gif_options = gif_options or {}
        try:
            self.writer = WRITERS[suffix]
        except:
            raise ValueError('Cannot write %s files' % suffix)

        filename = os.path.expanduser(os.path.abspath(filename))
        file_root = filename[:-4] if filename.endswith(suffix) else filename
        self.filename = file_root + suffix
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)

        if tmp_dir:
            self.tmp_dir_name = tmp_dir
            if remove_tmp_dir:
                shutil.rmtree(tmp_dir, ignore_errors=True)
            os.makedirs(self.tmp_dir_name, exist_ok=True)
        else:
            self.tmp_dir = tempfile.TemporaryDirectory()
            self.tmp_dir_name = self.tmp_dir.name
        self.basename = os.path.basename(file_root)
        self.finished = False
        self.stop_after_write = True
        self.times = []

    def set_project(self, project):
        self.project = project
        self.render = renderer.renderer(project.layout, **self.render)
        assert self.render

    def step(self, cur_step):
        if self.finished or (self.divide >= 1 and cur_step % self.divide):
            return True

        frame = cur_step / max(self.divide, 1)
        self.times.append(self.project.time())

        if self.time:
            elapsed = self.times[-1] - self.times[0]
            self.finished = (elapsed >= self.time)
        else:
            self.finished = (frame >= self.frames)

        if self.finished:
            self.write()
            return True

        frame_name = '%s%04d.png' % (self.basename, frame)
        filename = os.path.join(self.tmp_dir_name, frame_name)

        self.render().save(filename)
        self.frame_files.append(filename)

    @property
    def fps(self):
        if self._fps:
            print('1')
            return self._fps

        if self.duration:
            print('2')
            return 1 / self.duration

        if len(self.frame_files) < 2:
            print('3')
            return 1

        dt = self.times[-1] - self.times[0]
        slots = len(self.frame_files) - 1
        print('4')
        return slots / dt

    @fps.setter
    def fps(self, fps):
        self._fps = fps

    def write(self):
        fps = self.fps * self.speed
        print('fps', fps)
        self.writer(self.filename, self.frame_files, fps, **self.gif_options)

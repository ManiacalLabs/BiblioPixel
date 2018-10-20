from . import gif


class Writer(gif.Writer):
    def __init__(self, writer):
        writer.gif_dir = writer.gif_dir or writer.basename
        super().__init__(writer)

    def write(self):
        pass

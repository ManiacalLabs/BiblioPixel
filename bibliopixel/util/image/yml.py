import itertools
from .. import data_file

MODULE = '.'.join(__name__.split('.')[:-1])

YML_READER_TYPE = MODULE + '.yml.Reader'
SEPARATOR = '---\n'
COLORS_PER_LINE = 12


class Writer:
    def __init__(self, movie_writer):
        self.shape = movie_writer.project.layout.shape
        self.ranges = tuple(range(i) for i in self.shape)
        self.getter = movie_writer.project.layout.get
        self.movie_writer = movie_writer
        self.fp = None

    def step(self):
        if not self.fp:
            self.fp = open(self.movie_writer.filename, 'w')
            header = {
                'typename': YML_READER_TYPE,
                'fps': self.movie_writer.scaled_fps,
                'shape': self.shape,
            }
            data_file.dump(header, self.fp)

        self.fp.write(SEPARATOR)
        self.fp.write('"')
        for i, index in enumerate(itertools.product(*self.ranges)):
            if not (i % COLORS_PER_LINE):
                self.fp.write('\\\n')
            self.fp.write('%02x%02x%02x' % self.getter(*index))
        self.fp.write('"\n')

    def write(self):
        try:
            self.fp.close()
        except:
            pass

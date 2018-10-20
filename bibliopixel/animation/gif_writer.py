from .. util import deprecated
if deprecated.allowed():
    from . movie_writer import MovieWriter as GifWriter

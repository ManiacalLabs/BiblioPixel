from .. import wrapper
from ... project import importer
from ... layout import cutter
from . import functions
from ... util import class_name


class MatrixIndexer:
    cutter_class = cutter.Indexer

    def __init__(self, layout, by_row=True, function=None):
        self.layout = layout
        self.cutter = self.cutter_class(layout, by_row)
        self.function = function or functions.sorter

    def __call__(self):
        self.cutter.apply(self.function)


class Reprocess(wrapper.Wrapper):
    def __init__(self, *args, process=None, **kwds):
        super().__init__(*args, **kwds)
        self.preclear = False

        pname = class_name.class_name(MatrixIndexer)

        process = process or pname
        if isinstance(process, str):
            typename = process
            process = {}
        else:
            typename = process.pop('typename', pname)

        datatype = importer.import_symbol(
            typename, 'bibliopixel.animation.reprocess')
        self.process = datatype(layout=self.layout, **process)

    def step(self, amt=1):
        super().step(amt)
        self.process()

import json
from . import files


class DataFile(object):
    def __init__(self, filename, open=files.opener):
        self.filename = filename

        self.open = open
        self.data = {}
        self.read()

    def read(self):
        try:
            fp = self.open(self.filename)
        except FileNotFoundError:
            self.data = {}
        else:
            self.data = json.load(fp)

    def write(self):
        json.dump(self.data, self.open(self.filename, 'w'))

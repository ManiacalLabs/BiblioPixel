import copy, json
from . import files


class DataFile(object):
    def __init__(self, filename, open=files.opener):
        self.filename = filename

        self.open = open
        self.read()

    def read(self):
        try:
            fp = self.open(self.filename)
        except FileNotFoundError:
            self.data = {}
        else:
            self.data = json.load(fp)

        self.data_as_read = copy.deepcopy(self.data)

    def write(self):
        if self.data != self.data_as_read:
            json.dump(self.data, self.open(self.filename, 'w'))
            self.data_as_read = copy.deepcopy(self.data)

    def get(self, key):
        return self.data.get(key)

    def set(self, key, value, write=True):
        self.data[key] = value
        write and self.write()

    def delete(self, key):
        del self.data[key]

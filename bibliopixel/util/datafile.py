import copy, json


class DataFile(object):
    def __init__(self, filename, open=open):
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

    def write(self):
        json.dump(self.data, self.open(self.filename, 'w'))

    def get(self, key):
        return self.data.get(key)

    def set(self, key, value):
        self.data[key] = value
        self.write()

    def delete(self, key):
        del self.data[key]
        self.write()

    def delete_all(self):
        self.data.clear()
        self.write()

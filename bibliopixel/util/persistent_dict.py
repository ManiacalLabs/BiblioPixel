import copy
from . import json


class PersistentDict(object):
    def __init__(self, filename):
        self.filename = filename
        self.read()

    def read(self):
        try:
            self.data = json.load(self.filename)
        except FileNotFoundError:
            self.data = {}

    def write(self):
        json.dump(self.data, self.filename)

    def get(self, key):
        return self.data.get(key)

    def set(self, key, value):
        self.data[key] = value
        self.write()

    def set_items(self, items):
        for k, v in items:
            self.data[k] = v
        self.write()

    def delete(self, key):
        del self.data[key]
        self.write()

    def delete_all(self):
        self.data.clear()
        self.write()

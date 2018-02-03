import os
from . import json


class PersistentDict(dict):
    """A dictionary that persists as a JSON file on the filesystem.

    PersistentDict is constructed with a filename, which either does not exist,
    or contains JSON representing a previously stored value.

    Each time a PersistentDict is mutated, the file is rewritten with the new
    stored JSON data.
    """

    def __init__(self, filename):
        """
        :param c: the filename to store the JSON in
        """
        self.__filename = filename
        data = json.load(filename) if os.path.exists(filename) else {}
        super().__init__(data)

    def clear(self):
        super().clear()
        self.__write()

    def pop(self, *args):
        super().pop(*args)
        self.__write()

    def popitem(self):
        super().popitem()
        self.__write()

    def update(self, *args, **kwds):
        super().update(*args, **kwds)
        self.__write()

    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise ValueError('Keys for PersistentDict must be strings')
        super().__setitem__(key, value)
        self.__write()

    def __delitem__(self, key):
        super().__delitem__(key)
        self.__write()

    def __write(self):
        json.dump(self, self.__filename)

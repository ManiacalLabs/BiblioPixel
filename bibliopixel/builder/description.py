import os
from . import sections
from .. project import aliases, importer, merge
from .. util import class_name, data_file, log


class Description:
    """
    Set and get project description, either as attributes or as indexes.

    Examples are :

    desc.run['threaded'] = True
    desc.animation = '.tests.PixelTester'
    """

    def __init__(self):
        self.clear()

    def clear(self):
        """Clear description to default values"""
        self._desc = {}
        for key, value in merge.DEFAULT_PROJECT.items():
            if key not in self._HIDDEN:
                self._desc[key] = type(value)()

    def items(self):
        """Return an iterable of (key, section value) pairs"""
        return self._desc.items()

    def update(self, desc=None, **kwds):
        """This method updates the description much like dict.update(), *except*:

        1. for description which have dictionary values, it uses update
           to alter the existing value and does not replace them.

        2. `None` is a special value that means "clear section to default" or
           "delete field".
        """
        sections.update(self._desc, desc, **kwds)

    def as_dict(self):
        """Returns a dictionary of non-empty description"""
        return {k: v for k, v in self.items() if v}

    @property
    def desc(self):
        return self._desc

    def __str__(self):
        return data_file.dumps(self.as_dict()).strip()

    _HIDDEN = 'maker', 'typename'
    _ATTRIBUTES = ()

    def __getitem__(self, key):
        return self._desc[key]

    def __setitem__(self, key, value):
        sections.set_one(self._desc, key, value)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError("'Description' has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        if key.startswith('_') or key in self._ATTRIBUTES:
            super().__setattr__(key, value)
        else:
            self[key] = value

    def __dir__(self):
        return sorted(super().__dir__() + list(self._desc))

    def __contains__(self, key):
        return key in self._desc

    def __iter__(self):
        return iter(self._desc)

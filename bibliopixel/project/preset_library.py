import copy

from ..util.datafile import DataFile

"""
The BP preset library is a JSON file with five named sections:

    project, driver, layout, animation, run.

Each section is a dictionary that maps a name to a dictionary called a "preset".

For each section, a special preset named "default" is used if none is specified,
or the system default is used if no preset named "default" exists.

If a library preset has a key "extends" then it extends and overrides
another setting in the same section.
"""


def get_setting(section, name):
    extensions = []

    while name:
        setting = section[name]
        extensions.append(setting)
        name = setting.get('extends')

    setting = {}
    for s in reversed(extensions):
        setting.update(s)

    try:
        del setting['extends']
    except KeyError:
        pass
    return setting


class PresetLibrary(DataFile):
    def _section(self, section):
        return self.data.setdefault(section, {})

    def get_setting(self, section, name):
        return get_setting(self._section(section), name)

    def get_value(self, section, name, key):
        return self.get_setting(section, name)[key]

    def set_setting(self, section, name, setting):
        self._section(section)[name] = setting
        self.write()

    def set_value(self, section, name, key, value):
        self._section(section).set_default(name, {})[key] = value
        self.write()

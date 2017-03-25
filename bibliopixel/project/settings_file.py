import copy

from ..util.datafile import DataFile

"""
The BP settings file is a dotfile with four sections:

    driver, led, animation, run.

Each section is a dictionary mapping setting names to settings dictionaries.

The setting named "default" is used if none is specified, or the system default
if no setting named "default" exists.

If a settings dictionary has the entry "extends" then it extends and overrides
another setting in the same dictionary.  The extends feature is transitive
but cannot be used recursively.
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


class SettingsFile(DataFile):
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

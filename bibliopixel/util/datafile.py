import configparser, json
from . import opener


def load_config(fp):
    interpolation = configparser.ExtendedInterpolation()
    parser = configparser.ConfigParser(interpolation=interpolation)

    parser.read_file(fp)

    return {k: dict(v) for k, v in parser.items() if dict(v)}


def dump_config(data, fp):
    parser = configparser.ConfigParser()
    for k, v in data.items():
        parser[k] = v

    parser.write(fp)


class DataFile(object):
    def __init__(self, filename, is_json=None, open=opener.opener):
        self.filename = filename

        if is_json is None:
            is_json = filename.endswith('.json')

        self.load = json.load if is_json else load_config
        self.dump = json.dump if is_json else dump_config
        self.open = open
        self.data = {}
        self.read()

    def read(self):
        try:
            fp = self.open(self.filename)
        except FileNotFoundError:
            self.data = {}
        else:
            self.data = self.load(fp)

    def write(self):
        self.dump(self.data, self.open(self.filename, 'w'))

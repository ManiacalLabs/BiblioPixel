import configparser, json


def read_config(fp):
    interpolation = configparser.ExtendedInterpolation()
    parser = configparser.ConfigParser(interpolation=interpolation)

    parser.read_file(fp)

    return {k: dict(v) for k, v in parser.items()}


def write_config(data, fp):
    parser = configparser.ConfigParser()
    for k, v in data.items():
        parser[k] = v

    parser.write(fp)


def reader_writer(filename, is_json=None, open=open):
    if is_json is None:
        is_json = filename.endswith('.json')

    read = json.load if is_json else read_config
    write = json.dump if is_json else write_config

    def reader():
        try:
            fp = open(filename)
        except FileNotFoundError:
            return {}
        return read(fp)

    def writer(data):
        return write(data, open(filename, 'w'))

    return reader, writer

import json
from ..project.defaults import SECTIONS

HELP = """
Set bibliopixel values
"""


def run(args, settings):
    parts = args.name.split('.')

    if len(parts) == 2:
        parts.append('')

    elif len(parts) != 3:
        print('ERROR: name must have 2 or 3 parts: %s' % args.name)
        return -1

    section, name, key = parts

    if section not in SECTIONS:
        print('ERROR: no section %s' % section)
        return -1

    sdict = settings.data.setdefault(section, {})

    if key:
        sdict.setdefault(name, {})[key] = args.value
    else:
        try:
            value = json.loads(args.value)
        except:
            print('ERROR: Can\'t parse json value: %s' % args.value)
            return -1

        if not isinstance(value, dict):
            print('ERROR: value must be a dictionary: %s' % args.value)
            return -1

        sdict[name] = value

    settings.write()


def set_parser(parser):
    parser.set_defaults(run=run)
    parser.add_argument('name')
    parser.add_argument('value')

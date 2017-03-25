from ..project.defaults import SECTIONS

HELP = """
Show bibliopixel settings.
"""


def run(args, settings):
    def show_all():
        if not settings.data:
            print('No settings.')
            return

        first = True
        for name, section in sorted(settings.data.items()):
            if first:
                first = False
            else:
                print()

            show_section(name, section)

    def show_section(name, section):
        print('%s:' % name)
        for i in sorted(section.keys()):
            print('    %s' % i)

    def show_setting(setting):
        for k, v in sorted(setting.items()):
            print('%s = %s' % (k, v))

    if not args.name:
        show_all()
        return

    parts = args.name.split('.')
    section_name = parts.pop(0)

    try:
        section = settings.data[section_name]
    except KeyError:
        print('ERROR: no section %s' % section_name)
        return -1

    if not parts:
        show_section(section_name, section)
        return

    name = parts.pop(0)
    try:
        setting = section[name]
    except KeyError:
        print('ERROR: no setting %s in section %s' % (section_name, section))
        return -1

    if not parts:
        show_setting(setting)
        return

    key = parts.pop(0)
    if parts:
        print('ERROR: too many segments in name %s' % args.name)
        return -1

    try:
        value = setting[args.key]
    except:
        print('ERROR: no key %s in setting %s in section %s' %
              (key, setting, section_name))
        return -1

    print(value)


def set_parser(parser):
    parser.set_defaults(run=run)
    parser.add_argument('name', nargs='?', default='')

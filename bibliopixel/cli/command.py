import operator


class Command(object):

    ''' A base class for Command parsers
    This class layout may or may not help organization and overall functionality of the command line interface operations
    '''
    name = ''
    description = ''
    parser = None

    def __init__(self, args):
        self.args = args

    def main(self):
        ''' Main method called when the command is called. '''
        raise NotImplementedError()

    def run(self):
        ''' Calls main() and handles interrupts and exceptions '''
        try:
            status = self.main()
        except KeyboardInterrupt as e:
            status = 1
        except Exception as e:
            status = '{} failed to run with exception: {}'.format(self.name, e)
        return(status)

    @classmethod
    def add_arguments(cls):
        ''' Add arguments to the parser of cls

        Usage:
          cls.parser.add_argument('-d', '--detach', ...)

        '''
        # TODO(Cosmo): Add subparser capabilities
        pass

    @classmethod
    def create_parser(cls, subparsers):
        ''' Creates an argparse parser for the class and returns the parser. '''
        cls.parser = subparsers.add_parser(cls.name, help=cls.description)
        cls.parser.set_defaults(command_class=cls)
        cls.add_arguments()
        return cls.parser

    @classmethod
    def help(cls):
        ''' Print the help of a class '''
        cls.parser.print_help()


def __get_available_commands(command_class):
    commands = sorted(command_class.__subclasses__(), key=operator.attrgetter('name'))
    for cmd in commands:
        commands.extend(__get_available_commands(cmd))
    return commands


def get_available_commands():
    return __get_available_commands(Command)


def get_available_command_names():
    return [cmd.name for cmd in get_available_commands()]


def get_command(command_name):
    for cmd in get_available_commands():
        if cmd.name == command_name:
            return cmd
    raise ValueError('Invalid command name: %s' % command_name)

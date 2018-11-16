import os, pathlib
from .. project.importer import import_module
from .. util import deprecated, log

COMMANDS = (
    'animations', 'all_pixel', 'all_pixel_test', 'clear_cache', 'demo',
    'devices', 'info', 'monitor', 'new', 'run')

if deprecated.allowed():  # pragma: no cover
    SIGNAL_COMMANDS = 'kill', 'pid', 'restart', 'shutdown'
    COMMANDS += SIGNAL_COMMANDS

MODULES = {c: import_module('bibliopixel.commands.' + c) for c in COMMANDS}

FILE = pathlib.Path(__file__).parent / 'commands.rst.tmpl'

HELP = FILE.open().read().format(
    command_count=len(COMMANDS),
    commands=[
        ', '.join(COMMANDS[0:8]),
        ', '.join(COMMANDS[8:])])

BP_HEADER = """
APPENDIX: ``bp <command> --help`` for each command
==================================================
"""

BP_TEMPLATE = """\
``bp {command}``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

{doc}

{description}
"""

SEPARATOR = """
------------------------------------

"""


def get_command_help(command):
    module = MODULES[command]
    return BP_TEMPLATE.format(
        command=command,
        module=module,
        doc=module.__doc__.strip(),
        description=getattr(module, 'DESCRIPTION', ''))


BP_HELP = SEPARATOR.join(get_command_help(c) for c in COMMANDS)


def print_help():
    log.printer(HELP)
    log.printer(BP_HEADER)
    log.printer(BP_HELP)


if __name__ == '__main__':
    print_help()

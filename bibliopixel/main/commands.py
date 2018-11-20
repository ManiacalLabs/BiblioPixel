import importlib, os, pathlib
from .. project.importer import import_module
from .. import commands
from .. util import log


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


def print_help():
    template_file = pathlib.Path(__file__).parent / 'commands.rst.tmpl'

    help_text = template_file.open().read().format(
        command_count=len(commands.COMMANDS),
        commands=commands.COMMANDS_PRINTABLE)

    log.printer(help_text)
    log.printer(BP_HEADER)
    for command in commands.COMMANDS:
        module = importlib.import_module('bibliopixel.commands.' + command)
        log.printer(BP_TEMPLATE.format(
            command=command,
            doc=module.__doc__.strip(),
            description=getattr(module, 'DESCRIPTION', '')))


if __name__ == '__main__':
    print_help()

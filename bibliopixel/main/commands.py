from .. project.importer import import_module

COMMANDS = (
    'all_pixel', 'all_pixel_test', 'clear_cache', 'color', 'demo',
    'devices', 'info', 'load', 'list', 'remove', 'reset', 'run', 'save', 'set',
    'show', 'update')

MODULES = {c: import_module('bibliopixel.main.' + c) for c in COMMANDS}

RST_HELP = """\
``bp`` - The BiblioPixel Project Runner
========================================

``bp`` is a command-line script installed with Bibliopixel.  It can run
projects and demos, configure hardware, save and load defaults, and more.

``bp`` takes one of {0} *commands*:
  {1}
  {2}

Some commands take *arguments* - often names of files.

Examples of ``bp`` commands and arguments
------------------------------------------

    bp info
    bp demo circle
    bp run foo.json bar.json
    bp foo.json bar.json      # run is the default command

The commands are summarized below, and you can get more detailed help about
each one by typing:

::

    bp <command> --help

or

::

    bp <command> -h

The ``bp`` command line
-------------------------

``bp`` commands have *flags* that control how ``bp`` runs its commands.

Examples of flags are -v, --verbose, --defaults, -d, --simpixel.  Flags either
start with -, for one letter flags, or -- for multi-letter flags.

Sometimes two flags have the same meaning, like --simpixel and -s,
--verbose and -v, or --dimensions and --dim.

Some flags take an argument, like --dim=160 or --loglevel=frame.
Other flags do not, like --verbose or -v.

A ``bp`` command line can optionally include a command, a list of arguments,
and a list of flags:

::

    bp [<command>] [<argument> ...] [<flag> ...]

Examples of ``bp`` command lines
--------------------------------

::

    bp info --help
    bp run -h
    bp info
    bp color "indian red 4"
    bp foo.json bar.json -v
    bp foo.json bar.json -v --numbers=float --dump --defaults=default.json
""".format(len(COMMANDS),
           ', '.join(COMMANDS[0:8]),
           ', '.join(COMMANDS[8:]))

HELP = RST_HELP.replace('\n::\n', '').replace('``', '`')

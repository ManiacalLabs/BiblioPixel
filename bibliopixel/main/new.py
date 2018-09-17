"""
Create a new BLiPS project
"""

import os, re, string
from .. util import log

DESCRIPTION = """
Example:

.. code-block: bash

    # Create a new project directory named my-project/ in the current directory
    bp new my-project

    # Create a new project directory named my-project/ in ~/projects
    bp new my-project ~/projects

"""

PUNCTUATION = '.-_'
LEGAL_CHARS = set(string.ascii_letters + string.digits + PUNCTUATION)
DIR_NAME = os.path.dirname(__file__)


def run(args):
    name = args.project_name
    bad = set(name) - LEGAL_CHARS
    if bad:
        raise ValueError('Bad characters in project: "%s"' % ''.join(bad))
    if not name[0].isalpha():
        raise ValueError('Project names must start with a character')

    directory = args.directory or name
    if os.path.exists(directory):
        raise ValueError('Directory "%s" already exists' % directory)

    os.makedirs(directory)
    words = _split_words(name)
    class_name = ''.join(w.capitalize() for w in words)
    py_name = name.replace('.', '_').replace('-', '_')

    context = {
        'class_name': class_name,
        'name': name,
        'py_name': py_name,
    }

    for template, out_file in TEMPLATES.items():
        out_file = out_file.format(**context)
        out_file = os.path.join(directory, out_file)
        tmpl_file = os.path.join(DIR_NAME, template)
        tmpl_data = open(tmpl_file).read()

        with open(out_file, 'w') as fp:
            fp.write(tmpl_data.format(**context))
            log.printer('Written', out_file)

    log.printer('Created new project in', directory)


def set_parser(parser):
    parser.set_defaults(run=run)
    parser.add_argument('project_name', help=PROJECT_NAME_HELP)
    parser.add_argument('directory', default='', nargs='?', help=DIRECTORY_HELP)


TEMPLATES = {
    'template/project.yml.tmpl': '{name}.yml',
    'template/animation.py.tmpl': '{py_name}.py',
}

PROJECT_NAME_HELP = """
The Name of the new BLiPS project you want to create.

A Project Name can contain letters, numbers, `-` or `_`. Nothing else is
allowed, which means no whitespace, "no `/`" and no `.`.

A project name must start with a letter.

Valid project names are:

* P
* project_name
* IHeartArea51

Invalid project names are:

* 23skidoo
* project.name
* _23skidoo

"""

DIRECTORY_HELP = """
Optional directory where you want to create the project.
If absent, use the name of the project as the directory name.
"""

_split_words = re.compile(r'''
    # Find words in a string. Order matters!
    [A-Z]+(?=[A-Z][a-z]) |  # All upper case before a capitalized word
    [A-Z]?[a-z]+ |  # Capitalized words / all lower case
    [A-Z]+ |  # All upper case
    \d+  # Numbers
''', re.VERBOSE).findall
# https://stackoverflow.com/a/41510011/43839

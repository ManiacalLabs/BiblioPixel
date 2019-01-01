#!/usr/bin/env python3

"""
Automatically make a new release version of BiblioPixel by editing CHANGELIST.md
and bibliopixel/VERSION
"""

import datetime, io, os, pathlib, subprocess, sys

DRY_RUN = False
ROOT = pathlib.Path(__file__).parents[2]
CHANGELIST_FILE = str(ROOT / 'CHANGELIST.md')
VERSION_FILE = str(ROOT / 'bibliopixel' / 'VERSION')


def new_version(new_version_string=''):
    def call(s, *args):
        return subprocess.check_call(s.split() + list(args))

    def split_version(s):
        return tuple(int(i) for i in s.split('.'))

    def open_write(f):
        # https://stackoverflow.com/questions/2536545/
        return io.open(f, 'w', newline='\n')

    old_version = split_version(open(VERSION_FILE).read())

    if new_version_string:
        if new_version_string.startswith('v'):
            new_version_string = new_version_string[1:]
        new_version = split_version(new_version_string)
    else:
        new_version = old_version[:2] + (old_version[2] + 1,)
        new_version_string = '.'.join(str(i) for i in new_version)

    assert new_version > old_version

    comments = []

    while True:
        comment = input('- ')
        if not comment:
            break
        comments.append('- ' + comment + '\n')

    if not comments:
        raise ValueError(
            'There must be at least one new change in CHANGELIST.md')

    with open_write(VERSION_FILE) as fp:
        fp.write(new_version_string)
        fp.write('\n')

    changelist = open(CHANGELIST_FILE).read()
    with open_write(CHANGELIST_FILE) as fp:
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        fp.write('## v%s - %s\n' % (new_version_string, date))
        for c in comments:
            fp.write(c)
        fp.write('\n')
        fp.write(changelist)

    commit_comment = 'v' + new_version_string
    call('git commit bibliopixel/VERSION CHANGELIST.md -m', commit_comment)
    call('git push')


if __name__ == '__main__':
    new_version(*sys.argv[1:])

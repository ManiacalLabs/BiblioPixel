# -*- coding: utf-8 -*-
'''
Prints version information
'''

from bibliopixel.cli import Command


class Remove(Command):
    name = 'remove'
    description = 'Remove a project default file'

    def main(self):
        raise(NotImplementedError())

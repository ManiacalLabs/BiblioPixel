# -*- coding: utf-8 -*-
'''
Prints version information
'''

from bibliopixel.cli import Command


class Load(Command):
    name = 'load'
    description = 'Load a saved project default file'

    def main(self):
        raise(NotImplementedError())

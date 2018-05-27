# -*- coding: utf-8 -*-
'''
Prints version information
'''

from bibliopixel.cli import Command


class Set(Command):
    name = 'set'
    description = 'Set some or all sections of the project defaults'

    def main(self):
        raise(NotImplementedError())

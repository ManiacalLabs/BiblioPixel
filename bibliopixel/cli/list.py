# -*- coding: utf-8 -*-
'''
Prints version information
'''

from bibliopixel.cli import Command


class List(Command):
    name = 'list'
    description = 'List all user project default files'

    def main(self):
        raise(NotImplementedError())

# -*- coding: utf-8 -*-
'''
Prints version information
'''

from bibliopixel.cli import Command


class Show(Command):
    name = 'show'
    description = 'Show all project default values'

    def main(self):
        raise(NotImplementedError())

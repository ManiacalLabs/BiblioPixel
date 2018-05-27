# -*- coding: utf-8 -*-
'''
Prints version information
'''

from bibliopixel.cli import Command


class Color(Command):
    name = 'color'
    description = 'Toggle between color names and color tuples'

    def main(self):
        raise(NotImplementedError())

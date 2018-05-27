# -*- coding: utf-8 -*-
'''
Prints version information
'''

from bibliopixel.cli import Command


class AllPixel(Command):
    name = 'all_pixel'
    description = 'Configure the AllPixel or similar module'

    def main(self):
        raise(NotImplementedError())

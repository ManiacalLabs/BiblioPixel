# -*- coding: utf-8 -*-
'''
Prints version information
'''

from bibliopixel.cli import Command


class Info(Command):
    name = 'info'
    description = 'Print information about BLiPS'

    def main(self):
        raise(NotImplementedError())

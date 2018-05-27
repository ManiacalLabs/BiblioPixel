# -*- coding: utf-8 -*-
'''
Prints version information
'''

from bibliopixel.cli import Command


class Demo(Command):
    name = 'demo'
    description = 'Run a BLiPS demo'

    def main(self):
        raise(NotImplementedError())

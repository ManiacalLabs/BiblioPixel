# -*- coding: utf-8 -*-
'''
Prints version information
'''

from bibliopixel.cli import Command


class Monitor(Command):
    name = 'monitor'
    description = 'Monitor a control source'

    def main(self):
        raise(NotImplementedError())

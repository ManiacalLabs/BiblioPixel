# -*- coding: utf-8 -*-
'''
Prints version information
'''

from bibliopixel.cli import Command


class Devices(Command):
    name = 'devices'
    description = 'Find serial devices and update serial device IDs'

    def main(self):
        raise(NotImplementedError())

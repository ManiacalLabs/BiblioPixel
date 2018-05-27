# -*- coding: utf-8 -*-
'''
Prints version information
'''

from bibliopixel.cli import Command


class Reset(Command):
    name = 'reset'
    description = 'Reset sections in the project defaults'

    def main(self):
        raise(NotImplementedError())

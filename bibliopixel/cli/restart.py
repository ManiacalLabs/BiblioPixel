# -*- coding: utf-8 -*-
'''
Prints version information
'''

from bibliopixel.cli import Command


class Restart(Command):
    name = 'restart'
    description = '''
    Send a restart signal to a BLiPS process running on this machine.
    '''

    def main(self):
        raise(NotImplementedError())

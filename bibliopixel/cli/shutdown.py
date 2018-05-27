# -*- coding: utf-8 -*-
'''
Prints version information
'''

from bibliopixel.cli import Command


class Shutdown(Command):
    name = 'shutdown'
    description = '''
    Send an interrupt signal to a BLiPS process running
    on this machine to kill it.
    '''

    def main(self):
        raise(NotImplementedError())

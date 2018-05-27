# -*- coding: utf-8 -*-
'''
Prints version information
'''

from bibliopixel.cli import Command


class PID(Command):
    name = 'pid'
    description = '''
    Print the process Id of the current bp instance that
    is running a project, if any.
    '''

    def main(self):
        raise(NotImplementedError())

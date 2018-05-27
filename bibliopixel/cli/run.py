# -*- coding: utf-8 -*-
'''
Prints version information
'''

from bibliopixel.cli import Command


class Run(Command):
    name = 'run'
    description = 'Run specified project from file or URL.'

    def main(self):
        raise(NotImplementedError())

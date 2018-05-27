# -*- coding: utf-8 -*-
'''
Prints version information
'''

from bibliopixel.cli import Command


class Save(Command):
    name = 'save'
    description = 'Save the current project defaults to a file.'

    def main(self):
        raise(NotImplementedError())

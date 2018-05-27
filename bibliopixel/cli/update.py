# -*- coding: utf-8 -*-
'''
Prints version information
'''

from bibliopixel.cli import Command


class Update(Command):
    name = 'update'
    description = 'Update BLiPS\'s dependencies'

    def main(self):
        raise(NotImplementedError())

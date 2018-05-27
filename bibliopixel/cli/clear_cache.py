# -*- coding: utf-8 -*-
'''
Prints version information
'''

from bibliopixel.cli import Command


class ClearCache(Command):
    name = 'clear_cache'
    description = 'Clear the loady git repository library cache'

    def main(self):
        raise(NotImplementedError())

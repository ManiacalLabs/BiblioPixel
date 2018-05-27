# -*- coding: utf-8 -*-
"""
Prints the help of a command, if any
"""

from bibliopixel.cli import Command, get_command


class Help(Command):
    name = "help"
    description = "Prints the help of a command"

    @classmethod
    def add_arguments(cls):
        cls.parser.add_argument('command', help="A valid BLiPS command")

    def main(self):
        cmd = get_command(self.args.command)
        cmd.help()

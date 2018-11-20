import os, pathlib

DIR = os.listdir(str(pathlib.Path(__file__).parent))
COMMANDS = [i[:-3] for i in DIR if i.endswith('.py') and not i.startswith('_')]
COMMANDS_LINES = COMMANDS[0:8], COMMANDS[8:]
COMMANDS_PRINTABLE = '\n'.join(', '.join(i) for i in COMMANDS_LINES)

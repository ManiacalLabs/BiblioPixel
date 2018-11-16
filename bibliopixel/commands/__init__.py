import os, pathlib

DIR = os.listdir(str(pathlib.Path(__file__).parent))
COMMANDS = [i[:-3] for i in DIR if i.endswith('.py') and not i.startswith('_')]

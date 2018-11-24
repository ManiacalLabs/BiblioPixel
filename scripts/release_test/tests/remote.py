import common

FEATURES = 'browser',
PROJECT = 'remote.yml'


def run():
    common.prompt('Open a simpixel browser window and press return')
    common.run_project(PROJECT)

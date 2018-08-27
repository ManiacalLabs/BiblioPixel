import common

FEATURES = 'browser',
PROJECT = 'remote.yml'


def run():
    input('Open a simpixel browser window and press return. ')
    common.run_project(PROJECT)

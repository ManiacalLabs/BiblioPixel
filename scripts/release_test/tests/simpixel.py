import common

FEATURES = 'browser',
PROJECTS = 'sim-strip.yml', 'sim-matrix.yml', 'sim-cube.yml', 'sim-circle.yml',


def run():
    input('Open a simpixel browser window and press return. ')
    common.run_project(*PROJECTS)

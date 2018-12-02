import common

FEATURES = 'browser',
PROJECTS = 'sim-strip.yml', 'sim-matrix.yml', 'sim-cube.yml', 'sim-circle.yml',


def run():
    common.test_prompt('simpixel')
    common.run_project(*PROJECTS, flag='-s')

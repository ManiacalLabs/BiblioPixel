import common

FEATURES = 'browser',
PROJECT = 'remote.yml'


def run():
    common.test_prompt('remote')
    common.run_project(PROJECT, flag='-s')

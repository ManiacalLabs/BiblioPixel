import common


def run():
    common.test_prompt('demo')
    for i, demo in enumerate(('bloom', 'circle', 'cube', 'matrix')):
        if i:
            common.execute('bp', 'demo', demo, '--pl=3', '--simpixel=no')
        else:
            common.execute('bp', 'demo', demo, '--pl=3')

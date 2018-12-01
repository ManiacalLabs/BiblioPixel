import common, os, shutil, yaml

FEATURES = ()
NEW_PROJECT_NAME = 'bp_new_project'


def run():
    def rm():
        if os.path.exists(NEW_PROJECT_NAME):
            shutil.rmtree(NEW_PROJECT_NAME)

    rm()
    try:
        common.execute('bp', 'new', NEW_PROJECT_NAME)
        base = '{0}/{0}'.format(NEW_PROJECT_NAME)
        common.execute('python', base + '.py')
        yaml.safe_load(open(base + '.yml'))

    finally:
        rm()

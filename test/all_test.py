import importlib, os, unittest

BLACKLIST = ['bibliopixel.drivers.PiWS281X']


def split_all(path):
    result = []
    old_path = None
    while path != old_path:
        (path, tail), old_path = os.path.split(path), path
        tail and result.insert(0, tail)
    return result


def get_imports():
    bp_root = os.path.dirname(os.path.dirname(__file__))
    python_root = os.path.join(bp_root, 'bibliopixel')
    for directory, sub_folders, files in os.walk(python_root):
        if '__' in directory:
            continue

        relative = os.path.relpath(directory, python_root)
        if relative == '.':
            root_import = 'bibliopixel'
        else:
            root_import = 'bibliopixel.' + '.'.join(split_all(relative))

        yield root_import

        for f in files:
            if f.endswith('.py') and '__' not in f:
                yield '%s.%s' % (root_import, f[:-3])


class ImportAllTest(unittest.TestCase):
    def test_all(self):
        failures = []
        for name in get_imports():
            if name in BLACKLIST:
                continue

            try:
                importlib.import_module(name)
            except:
                failures.append(name)
        self.assertEqual(failures, [])

        with open('/tmp/imports.txt', 'w') as f:
            for name in get_imports():
                f.write(name)
                f.write('\n')

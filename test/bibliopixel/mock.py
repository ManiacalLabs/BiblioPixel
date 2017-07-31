from argparse import Namespace


class MockFP(object):
    def __init__(self, filename, context):
        self.filename = filename
        self.context = context
        self.write_started = False

    def read(self):
        return self.context[self.filename]

    def write(self, x):
        if self.write_started:
            self.context[self.filename] += x
        else:
            self.write_started = True
            self.context[self.filename] = x

    def __iter__(self):
        return iter(self.read().splitlines())


def mock_open(context):
    def open(filename, access='r'):
        return MockFP(filename, context)

    return open

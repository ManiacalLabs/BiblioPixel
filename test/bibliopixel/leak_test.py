import gc, sys, time, unittest, weakref
from bibliopixel import builder
from bibliopixel.project import project


class TestLeaks(unittest.TestCase):
    def test_leaks(self):
        def _get_items():
            items, stops = [], []
            for creator in _CREATORS:
                item, stop = creator()
                items.append(item)
                stops.append(stop)
            [stop() for stop in stops]
            return weakref.WeakSet(items)

        items = _get_items()
        _pause()
        # If this next line were uncommented, it would work without all the
        # weakrefs in the code.
        # gc.collect()
        self.assertEqual(list(items), [])


def _pause():
    time.sleep(0.1)


def _builder_simple():
    b = builder.Builder(shape=8, driver='dummy')
    b.start(True)
    _pause()
    return b, b.stop


def _builder_project():
    b, stop = _builder_simple()
    return b.project, stop


def _project_simple():
    desc = {'shape': 8, 'driver': 'dummy', 'run': {'threaded': True}}
    p = project.project(desc)
    p.start()
    _pause()
    return p, p.stop


_CREATORS = _builder_simple, _builder_project, _project_simple

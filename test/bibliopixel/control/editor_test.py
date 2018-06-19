import unittest
from bibliopixel.control.editor import Editor
from bibliopixel.project.edit_queue import EditQueue


class Base:
    class Foo:
        def __init__(self):
            self.foo = 12

    class Bar:
        def __init__(self):
            self.foo = Base.Foo()

    class BarQ(Bar):
        def __init__(self):
            super().__init__()
            self.edit_queue = EditQueue()

    class Baz:
        def __init__(self):
            self.bar = Base.Bar()
            self.barq = Base.BarQ()
            self.bing = 15

    def __init__(self):
        self.baz = Base.Baz()


class EditorTest(unittest.TestCase):
    def test_no_queue(self):
        test = Base()
        qa = Editor('baz.bar.foo.foo')
        qa.set_root(test)
        self.assertEqual(qa.get(), 12)
        qa.receive(('hello', ))
        self.assertEqual(qa.get(), 'hello')

    def test_with_queue(self):
        test = Base()
        qa = Editor('baz.barq.foo.foo')
        qa.set_root(test)
        self.assertEqual(qa.get(), 12)
        qa.receive(('hello',))
        self.assertEqual(qa.get(), 12)
        test.baz.barq.edit_queue.get_and_run_edits()
        self.assertEqual(qa.get(), 'hello')

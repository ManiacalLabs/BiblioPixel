import queue
from . import (
    attributes, construct, cleanup, defaults, event_queue, load, recurse)
from .. util import exception, json
from .. animation import Animation, failed

EVENT_QUEUE_MAXSIZE = 1000


class Project:
    CHILDREN = 'maker', 'drivers', 'layout', 'animation', 'controls'

    @staticmethod
    def pre_recursion(desc):
        return cleanup.cleanup(desc)

    def construct_child(self, datatype, typename=None, **kwds):
        construct = getattr(datatype, 'construct', None)
        if construct:
            return construct(self, **kwds)
        return datatype(**kwds)

    def __init__(self, *,
                 drivers, layout, maker, path, animation, controls,
                 event_queue_maxsize=EVENT_QUEUE_MAXSIZE, **kwds):
        """
        :param int event_queue_maxsize: maxsize parameter to queue.Queue.
            0 means an unbounded queue.
        """
        def post(desc):
            return self.construct_child(**desc)

        def create(root, name, recover=None):
            with exception.add('Unable to create ' + name):
                return recurse.recurse(
                    root,
                    pre=None,
                    post=post,
                    python_path='bibliopixel.' + name,
                    recover=recover)

        attributes.check(kwds, 'project')
        self.path = path
        layout = layout or cleanup.cleanup_layout(animation)

        self.maker = self.construct_child(**maker)
        self.drivers = [create(d, 'drivers') for d in drivers]
        with exception.add('Unable to create layout'):
            self.layout = self.construct_child(**layout)

        def Failed(*args):
            return failed.Failed(self.layout, *args)

        self.animation = create(animation, 'animation', Failed)

        self.event_queue = event_queue.EventQueue(maxsize=event_queue_maxsize)
        self.animation.preframe_callback = self.event_queue.get_and_run_events

        # Unfortunately, the whole animation cycle is controlled by methods on
        # the topmost animation - but we need to get called back at a certain
        # point in that animation cycle in order to run the event queue safely -
        # and animations don't know about the Project!
        #
        # So the monkey-patch above.  Ugly.  When we rewrite the
        # animation cycle, it will be freed from the topmost animation, and
        # this problem will go away.  (Also, animations should have access to
        # the Project, but that's a whole separate issue.)

        self.controls = [create(c, 'control') for c in controls]

    def start(self):
        self.layout.start()
        for c in self.controls:
            c.start(self)
        self.animation.start()

    def cleanup(self):
        self.animation.cleanup()
        for c in self.controls:
            c.cleanup()
        self.layout.cleanup_drivers()

    def run(self):
        try:
            self.start()
        finally:
            self.cleanup()

    def deferred_set(self, address, *value):
        """
        Use an Address to set a value within the project, but defer it to
        happen on the event queue.
        """
        self.event_queue.put_event(address.set, self, *value)


def project(*descs, root_file=None):
    """
    Make a project with recursion and alias resolution.  Use this
    instead of calling Project() directly.
    """
    desc = defaults.merge(*descs)

    load.ROOT_FILE = root_file
    with load.extender(desc.get('path', '')):
        desc = recurse.recurse(desc)

    project = construct.construct(**desc)
    project.desc = desc
    return project

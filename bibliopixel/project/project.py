import queue, weakref
from . import (
    attributes, construct, cleanup, defaults, event_queue, load, recurse)
from .. util import exception, json, log

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
            exception = desc.get('_exception')
            if exception:
                raise exception
            return self.construct_child(**desc)

        def create(root, name):
            with exception.add('Unable to create ' + name):
                return recurse.recurse(
                    root,
                    pre=None,
                    post=post,
                    python_path='bibliopixel.' + name)

        attributes.check(kwds, 'project')
        self.path = path
        layout = layout or cleanup.cleanup_layout(animation)
        self.maker = self.construct_child(**maker)
        self.drivers = [create(d, 'drivers') for d in drivers]
        with exception.add('Unable to create layout'):
            self.layout = self.construct_child(**layout)

        self.animation = create(animation, 'animation')

        eq = event_queue.EventQueue(maxsize=event_queue_maxsize)
        self.layout.event_queue = self.animation.event_queue = eq
        self.animation.preframe_callback = eq.get_and_run_events

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
        self.PROJECTS_RUNNING.add(self)
        self.layout.start()
        for c in self.controls:
            c.set_root(self)
            c.start()
        self.animation.start()

    def stop(self):
        try:
            self.PROJECTS_RUNNING.remove(self)
        except KeyError:
            return
        log.debug('Project %s stop called', self)

        self.animation.stop()
        for c in self.controls:
            c.stop()
        self.layout.stop()

    def cleanup(self):
        self.animation.cleanup()
        for c in self.controls:
            c.cleanup()
        self.layout.cleanup_drivers()

    def join(self, timeout=None):
        self.animation.join(timeout)

        # TODO: This is a hack.  We only need to do this because we don't
        # know if we exited through stop(), or naturally through running out of
        # the thread.
        self.stop()

        for c in self.controls:
            c.join(timeout)
        self.layout.join(timeout)

    def run(self):
        try:
            self.start()
            self.join()
        finally:
            self.cleanup()
        log.debug('Project %s finishes run()', self)

    @staticmethod
    def stop_all():
        for p in list(Project.PROJECTS_RUNNING):
            p.stop()
        Project.PROJECTS_RUNNING.clear()

    PROJECTS_RUNNING = weakref.WeakSet()


def project(*descs, root_file=None):
    """
    Make a new project, using recursion and alias resolution.

    Use this function in preference to calling Project() directly.
    """
    load.ROOT_FILE = root_file

    desc = defaults.merge(*descs)

    with load.extender(desc.get('path', '')):
        desc = recurse.recurse(desc)

    project = construct.construct(**desc)
    project.desc = desc
    return project

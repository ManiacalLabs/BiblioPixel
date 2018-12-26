import atexit, os, queue, threading, time, traceback, weakref
from . import (
    attributes, clock, construct, edit_queue, fill, load, merge, recurse)
from .. util import exception, log

EDIT_QUEUE_MAXSIZE = 1000
NO_DATATYPE_ERROR = 'No "datatype" field in section "%s"'
MIN_TIME = 0.0001


class Project:
    CHILDREN = 'maker', 'drivers', 'layout', 'animation', 'controls'
    LOCK = threading.Lock()

    @staticmethod
    def pre_recursion(desc):
        return fill.fill(desc)

    def construct_child(self, section_name, datatype=None, typename=None,
                        **kwds):
        if not datatype:
            raise ValueError(NO_DATATYPE_ERROR % section_name)

        construct = getattr(datatype, 'construct', None)
        if construct:
            return construct(self, **kwds)
        return datatype(**kwds)

    def __init__(self, *,
                 drivers, layout, maker, path, animation, controls,
                 edit_queue_maxsize=EDIT_QUEUE_MAXSIZE, **kwds):
        """
        :param int edit_queue_maxsize: maxsize parameter to queue.Queue.
            0 means an unbounded queue.
        """
        self.needs_cleanup = False

        def create(root, name):
            def post(desc):
                exception = desc.get('_exception')
                if exception:
                    raise exception
                return self.construct_child(name, **desc)

            with exception.add('Unable to create ' + name):
                return recurse.recurse(
                    root,
                    pre=None,
                    post=post,
                    python_path='bibliopixel.' + name)

        attributes.check(kwds, 'project')
        self.path = path
        layout = layout or fill.fill_layout(animation)
        self.maker = self.construct_child('maker', **maker)
        self.drivers = [create(d, 'drivers') for d in drivers]
        with exception.add('Unable to create layout'):
            self.layout = self.construct_child('layout', **layout)

        self.animation = create(animation, 'animation')
        self.running = False
        self.clock = clock.Clock()

        eq = edit_queue.EditQueue(maxsize=edit_queue_maxsize)
        self.layout.edit_queue = self.animation.edit_queue = eq
        self.animation.add_preframe_callback(eq.get_and_run_edits)

        # Unfortunately, the whole animation cycle is controlled by methods on
        # the topmost animation - but we need to get called back at a certain
        # point in that animation cycle in order to run the edit queue safely -
        # and animations don't know about the Project!
        #
        # So the monkey-patch above.  Ugly.  When we rewrite the
        # animation cycle, it will be freed from the topmost animation, and
        # this problem will go away.

        self.controls = [create(c, 'control') for c in controls]

        for d in self.drivers:
            d.set_project(self)

        self.animation.set_project(self)

    def __del__(self):
        try:
            self.cleanup()
        except:
            traceback.print_exc()

    def start(self):
        with self.LOCK:
            if self.running:
                return

            self.running = True
            self.PROJECTS_RUNNING.add(self)

        self.needs_cleanup = True
        weak = weakref.ref(self)

        def cleanup_fn():
            w = weak()
            w and w.cleanup()

        atexit.register(cleanup_fn)
        self._cleanup_fn = cleanup_fn

        self.layout.start()
        for c in self.controls:
            c.set_project(self)
            c.start()
        self.animation.start()

    def stop(self):
        with self.LOCK:
            if not self.running:
                return
            self.running = False
            self.PROJECTS_RUNNING.remove(self)

        log.debug('Project %s stop called on pid %d', self, os.getpid())

        self.animation.stop()
        for c in self.controls:
            c.stop()
        self.layout.stop()
        return True

    def cleanup(self):
        if not self.needs_cleanup:
            return

        self.needs_cleanup = False
        atexit.unregister(self._cleanup_fn)
        self.animation.cleanup()
        for c in self.controls:
            c.cleanup()
        self.layout.cleanup_drivers()

    def join(self, timeout=None):
        self.animation.join(timeout)
        self.stop()

        for c in self.controls:
            c.stop_event.wait()
        self.layout.join(timeout)

    def run(self):
        try:
            self.start()
            self.join()
        finally:
            self.cleanup()
        log.debug('Project %s finishes run()', self)

    def flat_out(self=0):
        self.clock.flat_out = True

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

    desc = merge.merge(merge.DEFAULT_PROJECT, *descs)
    path = desc.get('path', '')

    if root_file:
        project_path = os.path.dirname(root_file)
        if path:
            path += ':' + project_path
        else:
            path = project_path

    with load.extender(path):
        desc = recurse.recurse(desc)

    project = construct.construct(**desc)
    project.desc = desc
    return project

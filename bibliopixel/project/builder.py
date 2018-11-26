import os, traceback, weakref
from . import aliases, importer, merge, project
from .. commands import animations
from .. drivers.SimPixel import driver as simpixel_driver
from .. util import class_name, data_file, log
from .. util.threads import runnable
from .. import colors

_HIDDEN = 'maker', 'typename'
_CLASS_SECTIONS = 'layout', 'animation', 'driver'


class Builder:
    """
    A Project Builder to allow people to experiment with projects
    from the command line or in their own main program.
    """
    COLORS = colors.COLORS

    def __init__(self, filename='', **kwds):
        self.description = {}
        self.project = None
        self.thread = None
        self.filename = filename
        if os.path.exists(filename):
            self.load(filename)
        else:
            self.filename = filename
            self._clear_description()
            if filename:
                log.info('New filename %s', filename)

        for k, v in kwds.items():
            setattr(self, k, v)

    def save(self, filename=''):
        """Save the project as a YML file.  Remembers the previous filename.
        Prompt if no file given."""
        self._load_save(filename, 'save')

    def load(self, filename=''):
        """Load or reload the project from a YML file.  Remembers the previous
        filename. Prompt if no file given.
        """
        self._load_save(filename, 'load')

    def start(self, threaded=None):
        """Creates and starts the project."""
        # Sadly, we can only run a single project at once.
        self.stop()
        if not Builder.running_builder():
            Builder._RUNNING_BUILDER = weakref.ref(self)
        elif Builder.INSTANCE() is not self:
            raise ValueError('Only one instance of Builder can run at once')

        if threaded is not None:
            self.threaded = threaded
        if self.threaded:
            self.thread = runnable.LoopThread()
            self.thread.run_once = self._run_once
            self.thread.start()
        else:
            self._run_once()
        return self

    def stop(self=None):
        """Stop the project if it's running"""
        self = self or Builder.running_builder
        if not self:
            return

        if self.project:
            try:
                self.project.stop()
            except:
                log.error('Error stopping project')
                traceback.print_exc()
            self.project = None
        if self.thread:
            try:
                self.thread.stop()
            except:
                log.error('Error stopping thread')
                traceback.print_exc()
            self.thread = None
        if Builder.running_builder() is self:
            Builder._RUNNING_BUILDER = None
        return self

    def copy(self):
        """
        Returns a copy of this Builder.  The project, the thread, and the
        filename are not copied, only the description. """
        return Builder(**self.description)

    def clear(self):
        """Stop the project if it's running and clear the project description"""
        self.stop()
        self._clear_description()
        return self

    @property
    def is_running(self):
        """
        Return True if the Builder is running, false otherwise.

        At most one Builder can be running at any time.
        """
        return bool(self.project)

    @property
    def threaded(self):
        return bool(self.run.get('threaded'))

    @threaded.setter
    def threaded(self, value):
        self.run['threaded'] = bool(value)

    @staticmethod
    def simpixel(new=0, autoraise=True):
        """Open an instance of simpixel in the browser"""
        simpixel_driver.open_browser(new=new, autoraise=autoraise)

    @staticmethod
    def animations():
        """List all the existing animations"""
        animations.run(None)

    @classmethod
    def running_builder(cls):
        """Return the unique Builder that is running, if any, or None"""
        return cls._RUNNING_BUILDER and cls._RUNNING_BUILDER()

    def __getattr__(self, k):
        if k not in self.description:
            return AttributeError("'Builder' has no attribute '%s'" % k)
        return self.description[k]

    def __setattr__(self, k, v):
        if k in self.ATTRIBUTES:
            super().__setattr__(k, v)

        elif k not in self.PROPERTIES:
            raise AttributeError('Cannot set key %s' % k)

        elif k not in _CLASS_SECTIONS or isinstance(v, dict):
            self.description[k] = v

        else:
            if isinstance(v, str):
                path = 'bibliopixel.' + k + ('s' if k == 'driver' else '')
                # Test to see it really exists
                rv = aliases.resolve(v)
                importer.import_symbol(rv, path)
            else:
                v = class_name.class_name(v)

            self.description.setdefault(k, {})['typename'] = v

    def __dir__(self):
        return sorted(super().__dir__() + list(self._PROPERTIES))

    def __repr__(self):
        parts = []
        if self.is_running:
            parts.append('Running')
        parts.append(super().__repr__())
        if self.filename:
            parts.append('from file')
            parts.append(self.filename)
        return ' '.join(parts)

    def __str__(self):
        return data_file.dumps(self._clean_description()).strip()

    def __add__(self, other):
        b = Builder()
        b += self
        b += other
        return b

    def __radd__(self, other):
        b = Builder()
        b += other
        b += self
        return b

    def __iadd__(self, other):
        if isinstance(other, dict):
            d = other
        elif isinstance(other, Builder):
            d = other.description
        elif isinstance(other, str):
            d = data_file.load(other)
        else:
            raise TypeError('Do not understand type %s' % type(d))

        self.description.update(d)
        return self

    def __copy__(self):
        return self.copy()

    def __deepcopy__(self, _):
        return self.copy()

    ATTRIBUTES = 'description', 'filename', 'project', 'thread', 'threaded'
    PROPERTIES = tuple(k for k in merge.DEFAULT_PROJECT if k not in _HIDDEN)
    _RUNNING_BUILDER = None

    def _run_once(self):
        try:
            descs = self.description, {'run': {'threaded': False}}
            log.info('Constructing project')
            self.project = project.project(*descs, root_file=self.filename)
            self.project.start()
        except:
            log.error(traceback.format_exc())
            raise
        finally:
            log.info('Project finished')
            self.stop()

    def _load_save(self, filename, action):
        filename = filename or self.filename
        if not filename:
            filename = input('Enter filename to %s: ' % action).strip()
            if not filename:
                log.info('%s aborted', action.capitalize())
                return
        if not filename.endswith('.yml'):
            filename += '.yml'

        if action == 'load':
            self._clear_description()
            self.description.update(data_file.load(filename))
        else:
            data_file.dump(self._clean_description(), filename)
        self.filename = filename

    def _clear_description(self):
        self.description = {}
        for key, value in merge.DEFAULT_PROJECT.items():
            if key not in _HIDDEN:
                if isinstance(value, (list, dict)):
                    value = type(value)()
                self.description[key] = value

    def _clean_description(self):
        return {k: v for k, v in self.description.items() if v}

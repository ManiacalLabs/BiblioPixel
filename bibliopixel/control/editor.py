from . address import number, Address
from . receiver import Receiver
from .. util import deprecated


class Editor(Receiver):
    """
    A `Editor` is a `Receiver` which gets and sets `Address`es, perhaps using an
    an optional `EditQueue` for the setting.

    When the `set_project` method is called, `Editor` searches
    down through the address and stores the most recent `edit_queue`
    method it finds.
    """

    def __init__(self, address=None, project=None):
        self.address = Address(address)
        if project is not None:
            self.set_project(project)

    def set_project(self, project):
        self.project = project
        self.segments = self.address.segments[:]
        self.last_segment = self.address.segments.pop()
        edit_queue = None

        for segment in self.address.segments:
            edit_queue = getattr(project, 'edit_queue', edit_queue)
            project = segment.get(project)

        self.edit_queue = edit_queue

    def receive(self, msg):
        """
        Receives a message, and either sets it immediately, or puts it on the
        edit queue if there is one.

        """
        if self.edit_queue:
            self.edit_queue.put_edit(self._set, msg)
        else:
            self._set(msg)

    def get(self):
        return self.last_segment.get(self._get())

    def set(self, value):
        self.receive((number(value),))

    def __bool__(self):
        return bool(self.address)

    def __str__(self):
        return str(self.address)

    def _get(self):
        project = self.project
        for segment in self.address.segments:
            project = segment.get(project)
        return project

    def _set(self, values):
        args = self.address.assignment + values
        self.last_segment.set(self._get(), *args)

    if deprecated.allowed():
        set_root = set_project

        @property
        def root(self):
            return self.project

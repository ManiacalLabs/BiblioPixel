from . address import number, Address
from . receiver import Receiver


class Editor(Receiver):
    """
    A `Editor` is a `Receiver` which gets and sets `Address`es, perhaps using an
    an optional `EditQueue` for the setting.

    When the `set_root` method is called, `Editor` searches
    down through the address and stores the most recent `edit_queue`
    method it finds.
    """

    def __init__(self, address=None, root=None):
        self.address = Address(address)
        if root is not None:
            self.set_root(root)

    def set_root(self, root):
        self.root = root
        self.segments = self.address.segments[:]
        self.last_segment = self.address.segments.pop()
        edit_queue = None

        for segment in self.address.segments:
            edit_queue = getattr(root, 'edit_queue', edit_queue)
            root = segment.get(root)

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
        root = self.root
        for segment in self.address.segments:
            root = segment.get(root)
        return root

    def _set(self, values):
        args = self.address.assignment + values
        self.last_segment.set(self._get(), *args)

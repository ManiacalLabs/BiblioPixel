from . address import Address
from . receiver import Receiver


class QueuedAddress(Receiver):
    """
    A `QueuedAddress` is a `Receiver` which sets `Address`es, perhaps using an
    an optional `EditQueue`.

    When the `set_root` method is called, `QueuedAddress` searches
    down through the address and stores the most recent `edit_queue`
    method it finds.

    """

    def __init__(self, address=None):
        self.address = Address(address)

    def set_root(self, root):
        self.last_segment = self.address.segments[-1]
        self.queue = None
        self.subroot = root

        for segment in self.address.segments:
            self.queue = getattr(self.subroot, 'edit_queue', self.queue)
            if segment is not self.last_segment:
                self.subroot = segment.get(self.subroot)
                if self.subroot is None:
                    raise ValueError(
                        'Resolving the address "%s" failed at "%s"' %
                        (self.address, segment))

    def receive(self, msg):
        """
        Receives a message, and either sets it immediately, or puts it on the
        edit queue if there is one.

        """
        if self.queue:
            self.queue.put_edit(self._set, msg)
        else:
            self._set(msg)

    def __bool__(self):
        return bool(self.address)

    def __str__(self):
        return str(self.address)

    def get(self):
        return self.last_segment.get(self.subroot)

    def _set(self, values):
        args = self.address.assignment + values
        self.last_segment.set(self.subroot, *args)

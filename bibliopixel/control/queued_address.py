from . address import Address
from . receiver import Receiver


class QueuedAddress(Receiver):
    """
    A `QueuedAddress` is a `Receiver` which sets `Address`es, perhaps using an
    an optional `EventQueue`.

    When the `set_target` method is called, `QueuedAddress` searches
    down through the address and stores the most recent `event_queue`
    method it finds.

    """
    def __init__(self, address=None):
        self.address = Address(address)

    def set_target(self, target):
        self.last_segment = self.address.segments[-1]
        self.queue = None
        self.subtarget = target

        for segment in self.address.segments:
            self.queue = getattr(self.subtarget, 'event_queue', self.queue)
            if segment is not self.last_segment:
                self.subtarget = segment.get(self.subtarget)

    def receive(self, msg):
        """
        Receives a message, and either sets it immediately, or puts it on the
        event queue if there is one.

        """
        if self.queue:
            self.queue.put_event(self._set, msg)
        else:
            self._set(msg)

    def __bool__(self):
        return bool(self.address)

    def __str__(self):
        return str(self.address)

    def get(self):
        return self.last_segment.get(self.subtarget)

    def _set(self, values):
        args = self.address.assignment + values
        self.last_segment.set(self.subtarget, *args)

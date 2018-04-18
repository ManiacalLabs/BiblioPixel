import abc


class Receiver(abc.ABC):
    """
    Several classes receive data and route it to a target, and this is their
    base class, mainly for documentation.

    Receivers must have two methods, `set_root` and `receive`.  `set_root`
    must be called exactly once for each Receiver, and this must be before
    `receive` is ever.
    """
    @abc.abstractmethod
    def set_root(self, root):
        pass

    @abc.abstractmethod
    def receive(self, values):
        pass

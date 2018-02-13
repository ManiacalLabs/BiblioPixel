import collections, functools, sys, threading
from . address import Address
from . extractor import Extractor
from . ops import Ops
from .. project import construct, importer
from .. util.log_errors import LogErrors


class OpsAddress(Address):
    def __init__(self, address, ops=()):
        super().__init__(address)
        self.ops = Ops(*ops)

    def set(self, target, first, *rest):
        if self.ops and not rest:
            super().set(target, self.ops(first))
        else:
            super().set(target, first, *rest)


class Controls:
    DEFAULT = {'datatype': OpsAddress}

    def __init__(self, routing, default=None, max_errors=16,
                 python_path='bibliopixel.controllers'):
        default = dict(self.DEFAULT, **(default or {}))
        self.routing = _make(routing, python_path, default, 'control')
        self.safe_receive = LogErrors(self.receive, max_errors)

    def start(self, target):
        self.target = target
        self.thread = self._make_thread()
        self.thread.start()

    def stop(self):
        self.thread.stop()

    def loop(self):
        for msg in self:
            self.safe_receive(msg)

    def receive(self, msg):
        """
        Receive a message from the input source.
        """
        routing, msg = self.routing, self._convert(msg)
        while routing and msg:
            if isinstance(routing, list):
                for address in routing:
                    address.set(self.target, *msg.values())
                return

            if isinstance(routing, dict):
                _, v = msg.popitem(last=False)
                routing = routing.get(str(v))
            else:
                raise ValueError('Unexpected type %s' % type(routing))

    def _convert(self, msg):
        """
        Convert the message to a new ``collections.OrderedDict``.
        """
        return collections.OrderedDict(msg)

    def __iter__(self):
        """Should yield a sequence of messages from the input source."""
        raise NotImplemented

    def _make_thread(self):
        """
        Returns the thread that run the loop for this control source.

        If the underlying source has its own thread or process, override this
        method.  The object returned needs to have two methods:  ``start()``
        and ``stop()``.
        """
        return threading.Thread(target=self.loop, daemon=True)


class ExtractedControls(Controls):
    EXTRACTOR = {}

    def __init__(self, extractor=None, **kwds):
        super().__init__(**kwds)
        extractor = dict(self.EXTRACTOR, **(extractor or {}))
        self._convert = Extractor(**extractor).extract


def _make(value, python_path, default, *keys):
    assert isinstance(default, dict)

    if isinstance(value, dict):
        if not (value.get('address') or value.get('typename')):
            return {k: _make(v, k, default, *keys) for k, v in value.items()}

        value = [value]

    elif isinstance(value, str):
        value = [{'address': value}]

    elif not isinstance(value, list):
        raise ValueError('Keyed value is not dict, list, or str',
                         '.'.join(reversed(keys)))

    result = []
    for v in value:
        result.append(construct.construct_type(dict(default, **v), python_path))

    return result

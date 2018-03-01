import collections, functools, sys, threading
from . address import Address
from . extractor import Extractor
from . ops import Ops
from .. project import construct, importer
from .. util.log_errors import LogErrors
from .. util import flatten, log, json


class OpsAddress(Address):
    def __init__(self, address, ops=()):
        super().__init__(address)
        self.ops = Ops(*ops)

    def set(self, project, *args):
        if args and self.ops and len(args) == 1:
            args = [self.ops(args[0])]
        return super().set(project, *args)


class Control:
    DEFAULT = {'datatype': OpsAddress}

    def __init__(self, routing, default=None, max_errors=16,
                 python_path='bibliopixel.control', verbose=False):
        default = dict(self.DEFAULT, **(default or {}))
        self.verbose = verbose
        routing = flatten.unflatten(routing)
        self.routing = _make(routing, python_path, default, 'control')
        self.safe_receive = LogErrors(self.receive, max_errors)

    def start(self, project):
        if self.verbose:
            log.info('Starting %s', self)
        self.project = project
        self.thread = self._make_thread()
        self.thread.start()

    def cleanup(self):
        self.stop()

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
        if self.verbose and log.is_debug():
            log.debug('Message %s', self._msg_to_str(msg))

        while routing:
            if isinstance(routing, list):
                if self.verbose:
                    log.info('Routed message %s to %s',
                             self._msg_to_str(msg), routing)
                for address in routing:
                    self.project.deferred_set(address, *msg.values())
                return

            if not msg:
                return
            if not isinstance(routing, dict):
                raise ValueError('Unexpected type %s' % type(routing))

            k, v = msg.popitem(last=False)
            routing = routing.get(str(v))

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

    def _msg_to_str(self, msg):
        return '.'.join(msg.values()) or '.'


class ExtractedControl(Control):
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

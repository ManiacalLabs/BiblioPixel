import collections, functools, sys, threading
from . extractor import Extractor
from .. project import construct, importer
from .. util.log_errors import LogErrors
from .. util import flatten, log, json
from . routing import ActionList, Routing


class Control:
    DEFAULT = {'datatype': ActionList}

    def __init__(self, routing=None, default=None, max_errors=16,
                 python_path='bibliopixel.control', verbose=False,
                 pre_routing=None):
        """
        :param Address pre_routing: This Address is set with with the message
            after the message is received and converted, but before it is
            routed.
        """
        self.verbose = verbose
        self.receive = LogErrors(self._receive, max_errors)
        default = dict(self.DEFAULT, **(default or {}))
        self.pre_routing = ActionList(pre_routing)
        self.routing = Routing(routing or {}, default or {}, python_path)
        self.running = False

    def start(self, project):
        if self.verbose:
            log.info('Starting %s', self)

        self.project = project  # Can I now delete this?
        self.pre_routing.set_target(project)
        self.routing.set_target(project)
        self.running = True
        self.thread = self._make_thread()
        self.thread.start()

    def cleanup(self):
        self.stop()

    def stop(self):
        self.running = False

    def loop(self):
        for msg in self:
            self.receive(msg)
            if not self.running:
                return

    def _receive(self, msg):
        """
        Receive a message from the input source and perhaps raise an Exception.
        """
        msg = self._convert(msg)

        str_msg = self.verbose and self._msg_to_str(msg)
        if self.verbose and log.is_debug():
            log.debug('Message %s', str_msg)

        if self.pre_routing:
            self.pre_routing.receive(msg)

        receiver, msg = self.routing.receive(msg)
        if receiver:
            receiver.receive(msg)
            if self.verbose:
                log.info('Routed message %s to %s', str_msg, receiver)

    def _convert(self, msg):
        """
        Convert the message to a Control-specific format
        """
        raise NotImplementedError

    def __iter__(self):
        """Should yield a sequence of messages from the input source."""
        raise NotImplementedError

    def _make_thread(self):
        """
        Returns the thread that run the loop for this control source.

        If the underlying source has its own thread or process, override this
        method.  The object returned needs to have two methods:  ``start()``
        and ``stop()``.
        """
        return threading.Thread(target=self.loop, daemon=True)

    def _msg_to_str(self, msg):
        if msg is None:
            return '(None)'
        return '.'.join(msg.values()) or '.'

    def __bool__(self):
        return bool(self.routing or self.pre_routing)


class ExtractedControl(Control):
    EXTRACTOR = {}

    def __init__(self, extractor=None, **kwds):
        super().__init__(**kwds)
        extractor = dict(self.EXTRACTOR, **(extractor or {}))
        self._convert = Extractor(**extractor).extract

import flask, werkzeug.serving
from werkzeug.datastructures import ImmutableOrderedMultiDict

from ... util import log
from ... util.threads import runnable
from ... animation.remote import opener


class OrderedFlask(flask.Flask):
    # http://flask.pocoo.org/docs/1.0/patterns/subclassing/

    class request_class(flask.Request):
        parameter_storage_class = ImmutableOrderedMultiDict


class Server(runnable.LoopThread):
    OPEN_DELAY = 1

    def __init__(self, port, external_access, open_page, **kwds):
        super().__init__()
        self.port = port
        self.hostname = '0.0.0.0' if external_access else 'localhost'
        self.app = OrderedFlask(__name__, **kwds)
        self.open_page = open_page

    def run_once(self):
        if self.open_page:
            opener.raw_opener('localhost', self.port, self.OPEN_DELAY)
        werkzeug.serving.run_simple(self.hostname, self.port, self.app)
        super().stop()

    def stop(self):
        def error():
            log.error('Unable to shut down REST server on port %d', self.port)

        super().stop()
        try:
            flask.request.environ.get('werkzeug.server.shutdown', error)()
        except Exception as e:
            log.debug('Exception shutting werkzeug down')

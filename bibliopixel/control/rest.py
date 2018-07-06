import contextlib, fractions, flask, http.client, traceback, werkzeug.serving
from . import control, editor
from .. util import log
from .. util.threads import runnable

PORT = 8787


class RestServer(runnable.LoopThread):
    def __init__(self, port, external_access, get, put):
        super().__init__()
        self.port = port
        self.hostname = '0.0.0.0' if external_access else 'localhost'
        self.app = flask.Flask(__name__)
        self.app.route('/')(lambda: 'BiblioPixel REST server')
        self.app.route('/get/<address>')(get)
        self.app.route('/put/<address>/<value>', methods=['GET', 'PUT'])(put)

    def run_once(self):
        werkzeug.serving.run_simple(self.hostname, self.port, self.app)
        super().stop()

    def stop(self):
        def error():
            log.error('Unable to shut down REST server on port %d', self.port)

        super().stop()
        try:
            flask.request.environ.get('werkzeug.server.shutdown', error)()
        except Exception as e:
            log.error('Exception shutting werkzeug down')


class Rest(control.ExtractedControl):
    """
    REST control that uses http GET and PUT commands to get and set values
    at Addresses in a Project.

    GET commands use the URL /get/<address> and return a JSON document
    containing the value at that address, if that exists.

    PUT commands use the URL /put/<address>/<value> and then set
    that address to be that value

    In the example projects/25-rest.yml, possible URLs might be:

        http://localhost:8787/get/animation.levels
        http://localhost:8787/put/animation.levels[2]/1
    """
    def __init__(self, *args, port=PORT, external_access=False, verbose=True,
                 **kwds):
        super().__init__(*args, verbose=verbose, **kwds)
        self.server = RestServer(port, external_access, self.get, self.put)

    def _make_thread(self):
        return self.server

    def get(self, address):
        ed = self._editor(address)
        with self._abort(http.client.BAD_REQUEST):
            return flask.jsonify(ed.get())

    def put(self, address, value):
        ed = self._editor(address)
        with self._abort(http.client.BAD_REQUEST):
            ed.set(value)
            return 'ok'

    def _editor(self, address):
        with self._abort(http.client.NOT_FOUND):
            ed = editor.Editor(address)
            ed.set_root(self.root)
            return ed

    @contextlib.contextmanager
    def _abort(self, code):
        try:
            yield
        except:
            if self.verbose:
                traceback.print_exc()
            flask.abort(code)

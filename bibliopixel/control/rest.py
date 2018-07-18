import contextlib, flask, fractions, functools, traceback
import http.client, werkzeug.serving
from werkzeug.datastructures import ImmutableOrderedMultiDict

from . import control, editor
from .. util import log
from .. util.threads import runnable

PORT = 8787

"""
The REST control opens four Endpoints that allow you to get and set Fields in
BiblioPixel Objects by Address.

* The **Basic Get Endpoint** and **Basic Set Endpoint** are simplified for
casual users.

* The **Single Endpoint** provides a REST API to `GET` and `PUT` a BiblioPixel
Object Field.

* The **Multi Endpoint** provides a REST-like API to `GET` and `PUT` multiple
BiblioPixel Object Fields.

---

The Basic Get Endpoint looks like /get/<address>.  It returns JSON
representing the BiblioPixel Object or Field at that Address.

The Basic Set Endpoint is /set/<address>/<value> - it sets a Field in a
BiblioPixel Object.

For casual use, the two Basic endpoints are easiest to use, because they
just respond to `GET` methods - "pasting a URL into a browser".

*Examples of Basic endpoints*

In the example projects/26-simple-rest.yml:

1. `http://localhost:8787/get/animation.levels` returns a JSON list of the
levels for each animation, `[0, 0, 0]` at the start.

2. `http://localhost:8787/set/animation.levels[2]/1` sets the level of the
third animation to be `1`.

---

The Single Endpoint, /single/<address>, provides a strict
`GET`/`PUT` REST API for one BiblioPixel Object or Field at a time.

With the `GET` method, this endpoint returns JSON representing the
whole Object or Field.

With the `PUT` method, it sets the value of a BiblioPixel Object Field
from the form data with key `"value"`.

*Examples of the Single endpoint*

Again looking at projects/26-simple-rest.yml:

1. `GET`ting `http://localhost:8787/single/animation.levels` again returns
`[0, 0, 0]` at the start.

2. `PUT`ting `http://localhost:8787/single/animation.levels[2]` with
form data `value=1` sets the level of the third animation to be `1`.

---

The Multi Endpoint, /multi or /multi/<address>, provides a `GET`/`PUT`
REST-like API for multiple BiblioPixel Objects or Fields at one time.

The `GET` method uses the keys in the HTTP request dictionary as
BiblioPixel Object or Field Addresses, and returns a dictionary
mapping the Addresses to their JSON values.

The `GET` method uses the keys and values in the HTTP request dictionary as
to set BiblioPixel Object Fields using the key as the Address.

If an `<address>` field is provided, then this is prepended onto each key.

*Examples of the Multi endpoint*

From projects/26-simple-rest.yml again:

1. `GET`ting `http://localhost:8787/multi` with form data
`animation.levels=0` again returns `animation.levels` or
`[0, 0, 0]` at the start.

2. `PUT`ting `http://localhost:8787/multi` with
form data `animation.levels=[1, 1, 1]&animation.master=0.5` sets the level of
all three animations to be `1`, and the `master` to be `0.5`.

3. `PUT`ting `http://localhost:8787/multi/master` with
form data `levels=[1, 1, 1]&master=0.5` does the same as the previous example.
"""


class OrderedFlask(flask.Flask):
    # http://flask.pocoo.org/docs/1.0/patterns/subclassing/

    class request_class(flask.Request):
        parameter_storage_class = ImmutableOrderedMultiDict


class RestServer(runnable.LoopThread):
    def __init__(self, port, external_access):
        super().__init__()
        self.port = port
        self.hostname = '0.0.0.0' if external_access else 'localhost'
        self.app = OrderedFlask(__name__)

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


def _single(method):
    """Decorator for Rest methods that take a single address"""
    @functools.wraps(method)
    def single(self, address, value=None):
        with self._abort(http.client.NOT_FOUND):
            ed = editor.Editor(address, self.root)

        with self._abort(http.client.BAD_REQUEST):
            if value is None:
                result = method(self, ed)
            else:
                result = method(self, ed, value)

            return flask.jsonify(result)

    return single


def _multi(method):
    """Decorator for Rest methods that take multiple addresses"""
    @functools.wraps(method)
    def multi(self, address=''):
        values = flask.request.values
        if address and values and not address.endswith('.'):
            address += '.'

        result = {}
        for a in values or '':
            try:
                ed = editor.Editor(address + a, self.root)
                result[address + a] = method(self, ed, a)
            except:
                if self.verbose:
                    traceback.print_exc()
                    log.error('Could not multi addr %s', a)

        return flask.jsonify(result)

    return multi


class Rest(control.ExtractedControl):
    def __init__(self, *args, port=PORT, external_access=False, verbose=True,
                 **kwds):
        super().__init__(*args, verbose=verbose, **kwds)
        self.server = RestServer(port, external_access)

        app = self.server.app
        app.route('/')(lambda: 'BiblioPixel REST server')

        # Basic Endpoints
        app.route('/get/<address>')(self.get)
        app.route('/set/<address>/<value>')(self.put)

        # GET endpoints
        app.route('/single/<address>')(self.get)

        app.route('/multi')(self.multi_get)
        app.route('/multi/<address>')(self.multi_get)

        # This is a GET endpoint that puts values to the server

        # PUT endpoints
        app.route('/single/<address>', methods=['PUT'])(self.single_put)

        app.route('/multi', methods=['PUT'])(self.multi_put)
        app.route('/multi/<address>', methods=['PUT'])(self.multi_put)

    def _make_thread(self):
        return self.server

    @_single
    def get(self, editor):
        return editor.get()

    @_single
    def put(self, editor, value):
        editor.set(value)
        return True

    @_single
    def single_put(self, editor):
        value = flask.request.values['value']
        editor.set(value)
        return True

    @_multi
    def multi_get(self, editor, address):
        return editor.get()

    @_multi
    def multi_put(self, editor, address):
        value = flask.request.values[address]
        editor.set(value)
        return True

    @contextlib.contextmanager
    def _abort(self, code):
        try:
            yield
        except:
            if self.verbose:
                traceback.print_exc()
            flask.abort(code)

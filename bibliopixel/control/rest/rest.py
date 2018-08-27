import contextlib, flask, functools, pathlib, traceback, urllib
import http.client
from . import server
from .. import control, editor
from ... util import data_file, log
from ... util.threads import runnable

PORT = 8787
ROOT_FOLDER = pathlib.Path(__file__).parents[3] / 'ui' / 'rest'
INDEX_FILE = 'index.html'
BAD_ADDRESS_ERROR = 'Bad address {address}'
BAD_GETTER_ERROR = 'Couldn\'t get address {address}'
BAD_SETTER_ERROR = 'Couldn\'t set value {value} at address {address}'


def _single(method):
    """Decorator for Rest methods that take a single address"""
    @functools.wraps(method)
    def single(self, address, value=None):
        address = urllib.parse.unquote_plus(address)
        try:
            error = BAD_ADDRESS_ERROR
            ed = editor.Editor(address, self.root)

            if value is None:
                error = BAD_GETTER_ERROR
                result = method(self, ed)
            else:
                error = BAD_SETTER_ERROR
                result = method(self, ed, value)
            result = {'value': result}

        except Exception as e:
            if self.verbose:
                traceback.print_exc()
            msg = '%s\n%s' % (error.format(**locals()), e)
            result = {'error': msg}

        return flask.jsonify(result)

    return single


def _multi(method):
    """Decorator for Rest methods that take multiple addresses"""
    @functools.wraps(method)
    def multi(self, address=''):
        values = flask.request.values
        address = urllib.parse.unquote_plus(address)
        if address and values and not address.endswith('.'):
            address += '.'

        result = {}
        for a in values or '':
            try:
                ed = editor.Editor(address + a, self.root)
                result[address + a] = {'value': method(self, ed, a)}
            except:
                if self.verbose:
                    traceback.print_exc()
                result[address + a] = {'error': 'Could not multi addr %s' % a}

        return flask.jsonify(result)

    return multi


class Rest(control.ExtractedControl):
    OPEN_PAGE = False

    def __init__(self, *args, port=PORT, external_access=False, verbose=True,
                 root_folder=ROOT_FOLDER, index_file=INDEX_FILE,
                 open_page=None, **kwds):
        super().__init__(*args, verbose=verbose, **kwds)

        root_folder = pathlib.Path(root_folder)
        index_file = pathlib.Path(index_file)
        if not index_file.is_absolute():
            index_file = root_folder / index_file
        self.index_file = str(index_file)

        static = str(root_folder / 'static')

        if open_page is None:
            open_page = self.OPEN_PAGE

        self.server = server.Server(
            port, external_access, open_page, static_folder=static)

        app = self.server.app
        app.route('/')(self.index)

        # Basic Endpoints
        app.route('/get/<address>')(self.get)
        app.route('/set/<address>/<value>')(self.put)
        # <address> and <value> are URL quoted

        # GET endpoints
        app.route('/single/<address>')(self.get)

        app.route('/multi')(self.multi_get)
        app.route('/multi/<address>')(self.multi_get)

        # PUT endpoints
        app.route('/single/<address>', methods=['PUT'])(self.single_put)

        app.route('/multi', methods=['PUT'])(self.multi_put)
        app.route('/multi/<address>', methods=['PUT'])(self.multi_put)

    def _make_thread(self):
        return self.server

    def index(self):
        with open(str(self.index_file)) as fp:
            return fp.read()

    @_single
    def get(self, editor):
        return self._get(editor)

    @_single
    def put(self, editor, value):
        unquoted = urllib.parse.unquote_plus(value)
        return self._set(editor, unquoted)

    @_single
    def single_put(self, editor):
        value = flask.request.values['value']
        return self._set(editor, value)

    @_multi
    def multi_get(self, editor, address):
        return self._get(editor)

    @_multi
    def multi_put(self, editor, address):
        value = flask.request.values[address]
        return self._set(editor, value)

    def _get(self, editor):
        return data_file.dumps(editor.get(), use_yaml=False)

    def _set(self, editor, value):
        loaded = data_file.loads(value)
        editor.set(loaded)
        return True

    @contextlib.contextmanager
    def _abort(self, code):
        try:
            yield
        except:
            if self.verbose:
                traceback.print_exc()
            flask.abort(code)


class OpenPage(Rest):
    OPEN_PAGE = True

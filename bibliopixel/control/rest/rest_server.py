import contextlib, flask, pathlib, traceback, urllib
from . import flask_server, method
from ... util import data_file


class RestServer:
    def __init__(self, port, external_access, open_page,
                 root_folder, index_file):
        root_folder = pathlib.Path(root_folder)
        static_folder = str(root_folder / 'static')

        index_file = pathlib.Path(index_file)
        if not index_file.is_absolute():
            index_file = root_folder / index_file
        self.index_file = str(index_file)

        self.project = None
        self.server = flask_server.FlaskServer(
            port, external_access, open_page, static_folder=static_folder)

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

    def index(self):
        with open(self.index_file) as fp:
            return fp.read()

    @method.single
    def get(self, editor):
        return self._get(editor)

    @method.single
    def put(self, editor, value):
        unquoted = urllib.parse.unquote_plus(value)
        return self._set(editor, unquoted)

    @method.single
    def single_put(self, editor):
        value = flask.request.values['value']
        return self._set(editor, value)

    @method.multi
    def multi_get(self, editor, address):
        return self._get(editor)

    @method.multi
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

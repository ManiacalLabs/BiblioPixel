import bibliopixel, flask, logging, os, queue, sys
from ... util import log

MESSAGE = """\
Remote UI Server available at: {1}
Local: http://localhost:{0}"""

EXTERNAL_ACCESS_MESSAGE = MESSAGE + """
External: http://<system_ip>:{0}"""

if '--verbose' not in sys.argv:
    logging.getLogger('werkzeug').setLevel(logging.ERROR)

ROOT_DIR = os.path.dirname(os.path.dirname(bibliopixel.__file__))
STATIC_DIR = os.path.join(ROOT_DIR, 'ui', 'web_remote')


class RemoteServer:
    def __init__(self, q_send, q_recv):
        assert os.path.exists(STATIC_DIR)
        self.app = flask.Flask('BP Remote', static_folder=STATIC_DIR)
        self._set_routes()
        self.q_send = q_send
        self.q_recv = q_recv

    @classmethod
    def shutdown_server(cls):
        log.warning('Shutting down UI server.')
        func = flask.request.environ.get('werkzeug.server.shutdown')
        if func is None:
            return False
        func()
        return True

    def _set_routes(self):
        self.app.route('/')(self.index)
        self.app.route('/<path:path>')(self.static_files)
        self.app.route('/run_animation/<string:animation>')(self.run_animation)
        self.app.route('/stop')(self.stop_animation)
        self.app.route('/api/<string:request>')(self.api)
        self.app.route('/api/<string:request>/<data>')(self.api)

    def index(self):
        log.debug('index.html')
        return self.app.send_static_file('index.html')

    def static_files(self, path):
        log.debug('static_files: %s', path)
        return self.app.send_static_file(path)

    def run_animation(self, animation):
        return self.api('run_animation', data=animation)

    def stop_animation(self):
        return self.api('stop_animation')

    def api(self, request, data=None):
        log.debug('api: %s, %s', request, data)
        msg = {
            'req': request.lower(),
            'data': data,
            'sender': 'RemoteServer'}

        self.q_send.put(msg)

        try:
            status, data = self.q_recv.get(timeout=5)
        except queue.Empty:
            status, data = False, 'Timeout waiting for response.'

        return flask.jsonify({
            'status': status,
            'msg': 'OK' if status else data,
            'data': data if status else None,
        })


def run_server(external_access, port, q_send, q_recv):
    server = RemoteServer(q_recv, q_send)
    if external_access:
        host_ip = '0.0.0.0'
        msg = EXTERNAL_ACCESS_MESSAGE
    else:
        host_ip = 'localhost'
        msg = MESSAGE

    log.info(msg.format(port, host_ip))

    import werkzeug.serving
    werkzeug.serving.run_simple(host_ip, port, server.app, threaded=True)

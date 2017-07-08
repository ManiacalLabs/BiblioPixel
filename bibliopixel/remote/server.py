from flask import Flask, jsonify
from werkzeug.serving import run_simple
import threading
import queue
import os


def fail(msg='Error'):
    return {
        'status': False,
        'msg': msg,
        'data': None
    }


def success(data=None, msg='OK'):
    return {
        'status': True,
        'msg': msg,
        'data': data
    }


class RemoteServer():
    def __init__(self, q_send, q_recv):
        self.__server_thread = None
        self.__recv_thread = None
        cdir = os.path.dirname(os.path.realpath(__file__))
        static_dir = os.path.join(cdir, 'static')
        print(static_dir)
        self.app = Flask('BP Remote', static_folder=static_dir)
        self._set_routes()
        self.q_send = q_send
        self.q_recv = q_recv

    def _set_routes(self):
        self.app.route('/')(self.index)
        self.app.route('/run_animation/<string:animation>')(self.run_animation)
        self.app.route('/stop')(self.stop_animation)
        self.app.route('/api/<string:request>')(self.api)
        self.app.route('/api/<string:request>/<data>')(self.api)

    def __recv(self):
        while True:
            obj = self.q_recv.get()
            print('Recv: {}'.format(obj))

    def index(self):
        # return "Test"
        return self.app.send_static_file('index.html')

    def run_animation(self, animation):
        resp = self.api('run_animation', data=animation)
        return resp

    def stop_animation(self):
        resp = self.api('stop_animation')
        return resp

    def __get_resp(self):
        try:
            status, data = self.q_recv.get(timeout=5)
            return success(data=data)
        except queue.Empty:
            return fail(msg='Timeout waiting for response.')

    def api(self, request, data=None):
        request = request.lower()
        self.q_send.put({'req': request, 'data': data})
        return jsonify(self.__get_resp())

    def run(self, external_access, port, ):
        host_ip = '0.0.0.0' if external_access else 'localhost'
        run_simple(host_ip, port, self.app, threaded=True)


def run_server(external_access, port, q_send, q_recv):
    server = RemoteServer(q_recv, q_send)
    server.run(external_access, port)

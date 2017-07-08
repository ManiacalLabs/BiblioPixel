import multiprocessing
import inspect
from .. animation import BaseAnimation
from . import server
from .. import log


DEFAULT_OFF = '**OFF**'


class RemoteControl():
    def __init__(self, animations, default=None):
        self.q_send = multiprocessing.Queue()
        self.q_recv = multiprocessing.Queue()
        self.server = multiprocessing.Process(target=server.run_server,
                                              args=(self.q_send, self.q_recv))

        if not isinstance(animations, dict):
            raise ValueError('animations must be a dict!')

        self.current_animation_name = None
        self.current_animation_obj = None
        self.animations = animations

        self.handlers = {}
        # TODO: More pythonic way to do this?
        for name, method in inspect.getmembers(self, predicate=inspect.ismethod):
            if name.startswith('handler_'):
                self.handlers[name.replace('handler_', '')] = method

        self.default = default
        if issubclass(type(self.default), BaseAnimation):
            self.animations[DEFAULT_OFF] = self.default
            self.default = DEFAULT_OFF

    def cleanup(self):
        self.q_recv.close()
        self.q_send.close()
        self.server.terminate()

    def __start_default(self):
        if self.default:
            self.__run_anim(self.default)

    def __stop_anim(self, run_default=False):
        if self.current_animation_obj:
            self.current_animation_obj.cleanup(clean_layout=False)
        if run_default:
            self.__start_default()

    def __start_anim(self, name):
        self.__stop_anim()
        self.__run_anim(name)

    def __run_anim(self, name):
        log.info('Running animation: {}'.format(name))
        self.current_animation_name = name
        self.current_animation_obj = self.animations[name]
        self.current_animation_obj.start()

    def handler_run_animation(self, name):
        if name not in self.animations:
            return False, 'Invalid animation name: {}'.format(name)
        else:
            self.__start_anim(name)
            return True, None

    def handler_stop_animation(self, data):
        self.__stop_anim(run_default=True)
        return True, None

    def handler_get_animations(self, data):
        lst = list(self.animations.keys())
        lst.remove(DEFAULT_OFF)
        return True, list(lst)

    def start(self):
        self.__start_default()
        self.server.start()
        while True:
            recv = self.q_recv.get()
            req = recv['req']
            if req not in self.handlers:
                resp = False, '{} is not a valid request!'.format(req)
            else:
                resp = self.handlers[req](recv['data'])
            self.q_send.put(resp)

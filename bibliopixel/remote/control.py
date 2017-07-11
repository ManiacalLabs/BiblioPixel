import multiprocessing
import inspect
from .. animation import BaseAnimation
from .. animation.animation import COMPLETE_REASON
from . import server
from .. import log


DEFAULT_OFF = 'OFF_ANIM'
DEFAULT_ANIM_CONFIG = {
    'bgcolor': '#00ff00',
    'font_color': '#ffffff',
    'display': None
}


class RemoteControl():
    def __init__(self, base_config, animations):
        # These start with the defaults
        self.config = {
            'title': 'BiblioPixel Remote',
            'bgcolor': '#000000',
            'font_color': '#ffffff',
            'external_access': False,
            'port': 5000
        }

        self.config.update(base_config)

        self.ui_config = {
            'bgcolor': self.config['bgcolor'],
            'title': self.config['title']
        }

        self.q_send = multiprocessing.Queue()
        self.q_recv = multiprocessing.Queue()

        server_args = (
            self.config['external_access'],
            self.config['port'],
            self.q_send,
            self.q_recv
        )

        self.server = multiprocessing.Process(target=server.run_server,
                                              args=server_args)

        if not isinstance(animations, list):
            raise ValueError('animations must be a list!')

        self.current_animation_name = None
        self.current_animation_obj = None
        self.animations = animations
        self.animation_objs = {}
        anim_list = []
        for anim in self.animations:
            anim_cfg = dict(DEFAULT_ANIM_CONFIG)
            anim_cfg.update(anim)
            if not anim_cfg['display']:
                anim_cfg['display'] = anim['name']
            anim_cfg['name'] = ''.join(e for e in anim['name'] if e.isalnum())
            anim_cfg['animation'].complete_callback = self.complete_callback
            self.animation_objs[anim_cfg['name']] = anim_cfg['animation']
            del anim_cfg['animation']  # no longer need here
            anim_list.append(anim_cfg)
        self.animations = anim_list

        self.handlers = {}
        # TODO: More pythonic way to do this?
        for name, method in inspect.getmembers(self, predicate=inspect.ismethod):
            if name.startswith('handler_'):
                self.handlers[name.replace('handler_', '')] = method

        self.default = base_config['default']
        if issubclass(type(self.default), BaseAnimation):
            self.animation_objs[DEFAULT_OFF] = self.default
            self.default = DEFAULT_OFF

        if self.default not in self.animation_objs:
            raise ValueError(('`{}` is not a valid default! '
                              'It must be one of the configured animation names.').format(self.default))

    def cleanup(self):
        self.q_recv.close()
        self.q_send.close()
        self.server.terminate()

    def complete_callback(self, reason):
        if reason != COMPLETE_REASON.CANCELED:
            self.__start_default()

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
        self.current_animation_obj = self.animation_objs[name]
        self.current_animation_obj.start()

    def handler_run_animation(self, name):
        if name not in self.animation_objs:
            return False, 'Invalid animation name: {}'.format(name)
        else:
            self.__start_anim(name)
            return True, None

    def handler_stop_animation(self, data):
        self.__stop_anim(run_default=True)
        return True, None

    def handler_get_config(self, data):
        resp = {
            'ui': self.ui_config,
            'animations': list(self.animations)
        }
        return True, resp

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

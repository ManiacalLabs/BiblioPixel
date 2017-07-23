import multiprocessing
from .. animation.animation import STATE
from .. animation import collection
from . import server
from .. import log


DEFAULT_OFF = 'OFF_ANIM'
DEFAULT_ANIM_CONFIG = {
    'bgcolor': '#00ff00',
    'font_color': '#ffffff',
    'display': None,
    'valid': True
}


OFF_ANIM = {
    'animation': 'bibliopixel.animation.off.OffAnim',
    'run': {'threaded': True}
}


BAD_DEFAULT_ERROR = """\
`{}` is not a valid default!
It must be one of the configured animation names."""


class RemoteControl(collection.Collection):
    def __init__(self, layout, animations,
                 external_access=False, port=5000,
                 title='BiblioPixel Remote', bgcolor='black',
                 font_color='white', default=None):

        self.internal_delay = 0  # never wait

        # normalize name and display first
        for anim in animations:
            anim['animation']['data'] = dict(DEFAULT_ANIM_CONFIG, **anim['animation'].get('data', {}))
            if not anim['animation'].get('name'):
                raise ValueError('All animations require the `name` parameter: {}'.format(anim['animation']))
            if not anim['animation']['data'].get('display'):
                anim['animation']['data']['display'] = anim['animation']['name']
            anim['animation']['name'] = ''.join(e for e in anim['animation']['name'] if e.isalnum())
            anim['run'] = anim.get('run', {})
            anim['run']['threaded'] = True  # threaded required
        super().__init__(layout, animations, True)

        self.name_map = {}
        self.anim_cfgs = []
        for i in range(len(self.animations)):
            anim = self.animations[i]
            name = animations[i]['animation']['name']  # if failed to load anim will be None
            animations[i]['animation']['data']['valid'] = (anim is not None)
            if name in self.name_map:
                raise ValueError('Cannot have multiple animations with the same name: ' + name)
            self.name_map[name] = None if anim is None else i
            self.anim_cfgs.append(animations[i]['animation']['data'])
            self.anim_cfgs[len(self.anim_cfgs) - 1]['name'] = name
            anim.on_completion = self.on_completion

        if default is None:
            self.default = DEFAULT_OFF
        else:
            self.default = ''.join(e for e in default if e.isalnum())
            self.name_map[DEFAULT_OFF] = self.name_map[self.default]
            if self.default is None:
                self.default = DEFAULT_OFF

        if self.default == DEFAULT_OFF:
            self.animations.append(self._make_animation(OFF_ANIM))
            self.name_map[DEFAULT_OFF] = len(self.animations) - 1

        self.index = self.name_map[DEFAULT_OFF]  # start with default animation

        self.ui_config = {
            'bgcolor': bgcolor,
            'font_color': font_color,
            'title': title
        }

        self.q_send = multiprocessing.Queue()
        self.q_recv = multiprocessing.Queue()

        server_args = (
            external_access,
            port,
            self.q_send,
            self.q_recv
        )

        self.server = multiprocessing.Process(target=server.run_server,
                                              args=server_args)

        self.handlers = {
            'run_animation': self.run_animation,
            'stop_animation': self.stop_animation,
            'get_config': self.get_config
        }

    def cleanup(self, clean_layout=True):
        self.q_recv.close()
        self.q_send.close()
        self.server.terminate()
        super().cleanup(clean_layout)

    def on_completion(self, reason):
        if reason != STATE.canceled:
            self.stop_animation()

    # API Handlers
    def run_animation(self, name=None):
        if name is None:
            name = self.default

        if name not in self.name_map:
            return False, 'Invalid animation name: {}'.format(name)

        if self.current_animation:
            self.current_animation.cleanup(clean_layout=False)
            self.index = -1

        log.info('Running animation: {}'.format(name))
        self.index = self.name_map[name]
        self.current_animation.start()
        return True, None

    def stop_animation(self, data):
        return self.run_animation()

    def get_config(self, data):
        resp = {
            'ui': self.ui_config,
            'animations': list(self.anim_cfgs)
        }
        return True, resp

    def pre_run(self):
        self.server.start()

    def step(self, amt=None):
        self.run_animation()
        while not self.threading.stop_event.isSet():
            recv = self.q_recv.get()
            req = recv['req']
            if req not in self.handlers:
                resp = False, '{} is not a valid request!'.format(req)
            else:
                resp = self.handlers[req](recv['data'])
            self.q_send.put(resp)

import multiprocessing
from .. animation.animation import STATE
from .. animation import collection
from . import server
from . import trigger_process
from .. util import log
from .. util import importer
import copy


DEFAULT_OFF = 'OFF_ANIM'
DEFAULT_ANIM_CONFIG = {
    'bgcolor': '#00ff00',
    'font_color': '#ffffff',
    'valid': True
}


OFF_ANIM = {
    'animation': 'bibliopixel.animation.off.OffAnim',
    'run': {'threaded': True}
}


BAD_DEFAULT_ERROR = """\
`{}` is not a valid default!
It must be one of the configured animation names."""


def normalize_name(name):
    return ''.join('_' if e is ' ' else e for e in name if e.isalnum() or e is ' ')


class RemoteControl(collection.Collection):
    def __init__(self, layout, animations,
                 external_access=False, port=5000,
                 title='BiblioPixel Remote', bgcolor='black',
                 font_color='white', default=None,
                 triggers=[]):

        self.internal_delay = 0  # never wait

        # normalize name and display first
        for i, anim in enumerate(animations):
            adesc = anim['animation']
            adesc['data'] = dict(DEFAULT_ANIM_CONFIG, **adesc.get('data', {}))
            if not adesc.get('name'):
                log.error('All animations should have the `name` parameter: {}'.format(adesc))
                adesc['name'] = str(i)
            adesc['data']['display'] = adesc['data'].get('display', adesc['name'])
            adesc['name'] = normalize_name(adesc['name'])
            anim['run'] = anim.get('run', {})
            anim['run']['threaded'] = True  # threaded required

        super().__init__(layout, copy.deepcopy(animations), True)

        self.name_map = {}
        self.anim_cfgs = []

        for i, anim in enumerate(self.animations):
            adesc = animations[i]['animation']
            name = adesc['name']  # if failed to load anim will be None
            if anim is None:
                adesc['data']['valid'] = False
                adesc['data']['display'] = 'LOAD FAILED: ' + adesc['data']['display']
                adesc['data']['bgcolor'] = 'rgb(48, 48, 48)'
                adesc['data']['font_color'] = 'white'

            if name in self.name_map:
                raise ValueError('Cannot have multiple animations with the same name: ' + name)
            self.name_map[name] = anim and i
            self.anim_cfgs.append(animations[i]['animation']['data'])
            self.anim_cfgs[-1]['name'] = name
            if anim:
                anim.on_completion = self.on_completion

        if default is None:
            self.default = DEFAULT_OFF
        else:
            self.default = normalize_name(default)
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

        self.q_recv = multiprocessing.Queue()

        self.send_queues = {
            'RemoteServer': multiprocessing.Queue()
        }

        server_args = (
            external_access,
            port,
            self.send_queues['RemoteServer'],
            self.q_recv
        )

        self.server = multiprocessing.Process(target=server.run_server,
                                              args=server_args)

        self.handlers = {
            'run_animation': self.run_animation,
            'stop_animation': self.stop_animation,
            'get_config': self.get_config,
            'trigger_animation': self.run_animation
        }

        self.trigger_procs = {}
        self.triggers = {}
        for trigger in triggers:
            typename = trigger.pop('typename')
            if typename:
                importer.import_symbol(typename)  # attempt early to fail early
                self.triggers.setdefault(typename, []).append(trigger)
            else:
                raise ValueError('Triggers require a `typename` field!')

        for typename, configs in self.triggers.items():
            self.trigger_procs[typename] = multiprocessing.Process(
                target=trigger_process.run_trigger,
                args=(typename, self.q_recv, configs))

    def cleanup(self, clean_layout=True):
        self.q_recv.close()
        for q in self.send_queues.values():
            q.close()
        self.server.terminate()
        for _, t in self.trigger_procs.items():
            t.terminate()
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
        for proc in self.trigger_procs.values():
            proc.start()

    def step(self, amt=None):
        self.run_animation()
        while not self.threading.stop_event.isSet():
            recv = self.q_recv.get()
            req = recv['req']
            if req not in self.handlers:
                resp = False, '{} is not a valid request!'.format(req)
            else:
                resp = self.handlers[req](recv['data'])

            resp_q = self.send_queues.get(recv['sender'])
            if resp_q:
                resp_q.put(resp)

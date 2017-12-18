import copy, multiprocessing
from . import server, trigger_process
from .. animation import STATE
from .. import collection
from ... project import load
from ... util import log
from bibliopixel.animation.off import OffAnim

DEFAULT_OFF = 'OFF_ANIM'
DEFAULT_ANIM_CONFIG = {
    'bgcolor': '#00ff00',
    'font_color': '#ffffff',
    'valid': True
}


BAD_DEFAULT_ERROR = """\
`{}` is not a valid default!
It must be one of the configured animation names."""


def normalize_name(name):
    return ''.join('_' if e is ' ' else e for e in name if e.isalnum() or e is ' ')


class RemoteControl(collection.Collection):
    @staticmethod
    def pre_recursion(desc):
        collection.Collection.pre_recursion(desc)

        animations = desc['animations']
        auto_demo = desc.pop('auto_demo', None)
        desc['anim_cfgs'] = []

        if auto_demo:
            auto_demo_run = auto_demo.pop('run', 10)  # default to 10 seconds per
            auto_demo['typename'] = 'sequence'
            auto_demo['data'] = dict(DEFAULT_ANIM_CONFIG, **auto_demo.get('data', {}))
            if 'name' not in auto_demo:
                auto_demo['name'] = 'DEMO_ANIM'
            auto_demo['data']['display'] = auto_demo['data'].get('display', auto_demo['name'])
            auto_demo['name'] = normalize_name(auto_demo['name'])
            auto_demo['animations'] = []
            animations.insert(0, {'animation': auto_demo, 'run': {'threaded': True}})

        # normalize name and display first
        for i, anim in enumerate(animations):
            anim['data'] = dict(DEFAULT_ANIM_CONFIG, **anim.get('data', {}))
            if not anim.get('name'):
                log.error('All animations should have the `name` parameter: {}'.format(anim))
                anim['name'] = str(i)
            anim['data']['display'] = anim['data'].get('display', anim['name'])
            anim['name'] = normalize_name(anim['name'])

            # This was originally done later as a side-effect.
            # Moved it here so it's obvious.  Seems like a defect - name is in
            # two places.
            anim['data']['name'] = anim['name']
            anim['run'] = anim.get('run', {})

            if auto_demo:
                demo_sub = copy.deepcopy(anim)
                demo_sub['run'].update(auto_demo_run)
                demo_sub['animation'].pop('name')
                demo_sub['animation'].pop('data')
                demo_sub['run']['threaded'] = False  # no threading allowed for internal sequences
                auto_demo['animations'].append(demo_sub)

            anim['run']['threaded'] = True  # threaded required
            desc['anim_cfgs'].append(anim['data'])

        return desc

    def __init__(self, *args, anim_cfgs,
                 external_access=False, port=5000,
                 title='BiblioPixel Remote', bgcolor='black',
                 font_color='white', default=None,
                 triggers=[], **kwds):
        super().__init__(*args, **kwds)
        self.internal_delay = 0  # never wait
        self.name_map = {}
        self.anim_cfgs = anim_cfgs

        for i, (anim, cfg) in enumerate(zip(self.animations, self.anim_cfgs)):
            name = cfg['name']
            if name in self.name_map:
                raise ValueError('Cannot have multiple animations with the same name: ' + name)
            if anim:
                anim.on_completion = self.on_completion
                self.name_map[name] = i
            else:
                # The animation failed to load.
                cfg.update(
                    valid=False,
                    display='FAILED: ' + cfg.get('display', '(no error)'),
                    bgcolor='rgb(48, 48, 48)',
                    font_color='white')
                self.name_map[name] = None

        if default is None:
            self.default = DEFAULT_OFF
        else:
            self.default = normalize_name(default)
            self.name_map[DEFAULT_OFF] = self.name_map[self.default]
            if self.default is None:
                self.default = DEFAULT_OFF

        if self.default == DEFAULT_OFF:
            off = OffAnim(self.layout)
            off.set_runner({'threaded': True})
            self.animations.append(off)
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
            'trigger_animation': self.run_animation,
            'brightness': self.change_brightness
        }

        self.trigger_procs = {}
        self.triggers = {}
        for trigger in triggers:
            typename = trigger.pop('typename')
            events = trigger.pop('events')
            if typename and events:
                load.code(typename)  # attempt early to fail early
                self.triggers.setdefault(typename, []).extend((events, trigger))
            else:
                raise ValueError('Triggers require `typename` and `events` fields!')

        for typename, trigger in self.triggers.items():
            events, kwargs = trigger
            self.trigger_procs[typename] = multiprocessing.Process(
                target=trigger_process.run_trigger,
                args=(typename, self.q_recv, events, kwargs))

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
            error = 'Invalid animation name: {}'.format(name)
            log.info(error)
            return False, error

        if self.current_animation:
            self.current_animation.cleanup(clean_layout=False)
            self.index = -1

        log.info('Running animation: {}'.format(name))
        self.index = self.name_map[name]
        self.current_animation.start()
        return True, None

    def stop_animation(self, data):
        return self.run_animation()

    def change_brightness(self, data):
        if isinstance(data, str):
            try:
                data = int(data)
            except:
                return False, 'Invalid brightness value!'

        self.layout.set_brightness(data)
        return True, None

    def get_config(self, data):
        resp = {
            'ui': self.ui_config,
            'brightness': self.layout.brightness,
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

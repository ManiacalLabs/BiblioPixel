import copy, multiprocessing
from . import opener, server, trigger_process
from .. animation import STATE
from .. import wrapper
from ... project import load
from ... util import log
from bibliopixel.animation.off import Off

DEFAULT_OFF = 'OFF_ANIM'
DEFAULT_ANIM_CONFIG = {
    'bgcolor': '#00ff00',
    'font_color': '#ffffff',
    'valid': True
}
DEFAULT_AUTO_DEMO_TIME = 10
DEFAULT_AUTO_DEMO_NAME = 'DEMO_ANIM'
OPENER_TIMEOUT = 2

BAD_DEFAULT_ERROR = """\
`{}` is not a valid default!
It must be one of the configured animation names."""


def normalize_name(name):
    return ''.join('_' if e is ' ' else e
                   for e in name
                   if e.isalnum() or e is ' ' or e is '_')


class RemoteControl(wrapper.Indexed):
    @staticmethod
    def pre_recursion(desc):
        wrapper.Indexed.pre_recursion(desc)

        animations = desc['animations']
        auto_demo = desc.pop('auto_demo', None)

        if auto_demo:
            auto_demo.setdefault('name', DEFAULT_AUTO_DEMO_NAME)
            animations.insert(0, auto_demo)

        desc['name_map'] = {}
        for i, anim in enumerate(animations):
            anim.setdefault('run', {}).update(threaded=True)

            display_name = anim.get('name') or str(i)

            anim['data'] = dict(DEFAULT_ANIM_CONFIG, **anim.get('data', {}))
            anim['data'].setdefault('display', display_name)

            # Get the normalized name - with only URL-safe characters in it.
            name = normalize_name(display_name)
            # It's a defect that we have name in two places but...?
            anim['name'] = anim['data']['name'] = name
            desc['name_map'][name] = i

        if len(desc['name_map']) < len(animations):
            log.warning('There are multiple animations with the same name. '
                        'Only the last will work.')

        if auto_demo:
            auto_demo.setdefault('typename', 'sequence')
            seconds = auto_demo['run'].pop('seconds', DEFAULT_AUTO_DEMO_TIME)
            auto_demo.setdefault('length', seconds)

            auto_demo['animations'] = [copy.deepcopy(a) for a in animations[1:]]
            for a in auto_demo['animations']:
                a['run']['threaded'] = False

            desc.setdefault('default', auto_demo['name'])

        default = desc.get('default', None)
        if default is not None:
            default = normalize_name(default)
            index = desc['name_map'].get(default)
            if index is None:
                log.warning('Do not understand default "%s"', default)
                log.warning('Names are %s', ', '.join(desc['name_map']))
            desc['default'] = index

        return desc

    def __init__(self, *args, name_map, external_access=False, port=5000,
                 title='BiblioPixel Remote', bgcolor='black',
                 font_color='white', default=None,
                 triggers=[], open_page=False, **kwds):
        super().__init__(*args, **kwds)
        self.internal_delay = 0  # never wait

        self.anim_cfgs = [a.data for a in self.animations]
        self.name_map = name_map
        self.port = port
        if open_page is False:
            self.open_page = False
        elif open_page is True:
            self.open_page = OPENER_TIMEOUT
        else:
            self.open_page = float(open_page)

        for anim in self.animations:
            anim.on_completion = self.on_completion

            if getattr(anim, 'empty', False):
                # The animation failed to load.
                display_name = anim.data.get('display', '(no error)')
                anim.data.update(
                    valid=False,
                    display='FAILED: ' + display_name,
                    bgcolor='rgb(48, 48, 48)',
                    font_color='white')

        if default is None:
            off = Off(self.layout)
            off._set_runner({'threaded': True})
            self.name_map[DEFAULT_OFF] = len(self.animations)
            self.animations.append(off)
        else:
            self.name_map[DEFAULT_OFF] = default

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
        if self.open_page is not False:
            opener.opener('localhost', port, self.open_page)

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
                raise ValueError(
                    'Triggers require `typename` and `events` fields!')

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
    def run_animation(self, name=DEFAULT_OFF):
        log.debug('run_animation %s', name)

        if name not in self.name_map:
            error = 'Invalid animation name: {}'.format(name)
            log.info(error)
            return False, error

        if self.current_animation:
            self.current_animation.cleanup(clean_layout=False)
            self.index = -1

        self.index = self.name_map[name]
        log.info('Running animation: {}'.format(name))
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
            'animations': self.anim_cfgs,
        }
        return True, resp

    def pre_run(self):
        self.server.start()
        for proc in self.trigger_procs.values():
            proc.start()

    def step(self, amt=None):
        if not self.cur_step:
            self.run_animation()
        super().step(amt)
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

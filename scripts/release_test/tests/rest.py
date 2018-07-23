import common
import contextlib, requests, subprocess, threading, time

FEATURES = 'browser',
START_BP = 'bp', '--loglevel=error', common.make_project('rest.yml')
STOP_BP = 'bp', 'shutdown'

ROOT = 'http://localhost:8787/'
PAUSE = 1


def get(name, url, method='GET'):
    common.printer(method, name + ':', requests.get(ROOT + url).json())


def put(name, url, data):
    resp = requests.put(ROOT + url, data=data or {})
    common.printer('PUT', name + ':', resp.text)


def bp(function):
    def wrapped():
        threading.Thread(
            target=subprocess.check_call, args=(START_BP,)).start()
        time.sleep(2 * PAUSE)

        function()
        subprocess.check_call(STOP_BP)

    return wrapped


@bp
def test_other():
    put('single', 'single/animation.levels', {'value': '[0, 0, 0]'})
    time.sleep(PAUSE)
    put('single', 'single/animation.levels', {'value': '[0, 1, 0]'})
    time.sleep(PAUSE)
    put('single', 'single/animation.levels', {'value': '[0, 0, 0]'})
    time.sleep(PAUSE)
    put('single', 'single/animation.levels', {'value': '[0, 1, 0]'})
    time.sleep(PAUSE)


@bp
def test_rest():
    time.sleep(PAUSE * 10)
    get('basic', 'get/animation.levels')
    get('single', 'single/animation.levels')
    get('multi', 'multi?animation.levels=0')
    get('multi2', 'multi/animation?levels=0')
    time.sleep(PAUSE)

    get('basic', 'set/animation.levels[0]/0', method='PUT')
    time.sleep(PAUSE)

    put('single', 'single/animation.levels[1]', {'value': 0})
    time.sleep(PAUSE)

    data = {'animation.levels[0]': 1, 'animation.levels[1]': 1,
            'animation.master': 0.5}
    put('multi', 'multi', data)
    time.sleep(PAUSE)

    put('multi', 'multi/animation', {'levels[0]': 0, 'master': 1.0})
    time.sleep(PAUSE)

    put('multi', 'multi/animation', {'levels': '[1, 1, 1]'})
    time.sleep(PAUSE)


def run():
    if True:
        test_rest()
    else:
        test_other()

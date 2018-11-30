import contextlib, os, signal
from . import log, pid_context

SIGNAL_NUMBERS = {k: v for k, v in signal.__dict__.items()
                  if k.startswith('SIG') and '_' not in k}

SIGNAL_NAMES = {v: k for k, v in SIGNAL_NUMBERS.items()}

STOP_SIGNALS = 'SIGINT', 'SIGTERM'
RESTART_SIGNALS = 'SIGHUP',
HANDLED_SIGNALS = STOP_SIGNALS + RESTART_SIGNALS


@contextlib.contextmanager
def context(**handlers):
    signals = {}

    def handler(signum, frame):
        signame = SIGNAL_NAMES[signum]
        signals[signame] = True
        handler = handlers[signame]
        handler()

    def set_all(handler):
        for signame in handlers:
            if signame in SIGNAL_NUMBERS:  # Windows doesn't have all signals
                signal.signal(SIGNAL_NUMBERS[signame], handler)

    set_all(handler)
    try:
        yield signals

    finally:
        set_all(signal.SIG_DFL)


def send_signal(sig, pid_filename=None):
    sig = SIGNAL_NUMBERS.get(sig, sig)

    if sig not in SIGNAL_NAMES:
        log.error('No signal %s', sig)
        return -1

    try:
        pid = pid_context.get_pid(pid_filename)
    except:
        log.error('No bp process running')
        log.debug('Could not find file %s', pid_filename)
        return -1

    try:
        os.kill(pid, sig)
    except:
        log.error('Failed to send signal %s to bp process %s', sig, pid)
        return -1

    log.info('%s sent to bp process %s', sig, pid)
    return 0


def run(filename, stopper,
        stop_signals=STOP_SIGNALS, restart_signals=RESTART_SIGNALS):
    signal_dict = {s: stopper for s in stop_signals + restart_signals}

    with pid_context.pid_context(filename):
        with context(**signal_dict) as signals:
            running = True
            while running:
                yield
                if not signals:
                    return
                log.info('Received signal %s', ' '.join(signals))
                running = all(s in restart_signals for s in signals)
                signals.clear()


def make_command(default_signal, help=''):
    # Handle legacy commands restart, kill, shutdown

    def add_arguments(parser):
        parser.add_argument(
            'signal', nargs='?', default=default_signal,
            choices=sorted(SIGNAL_NUMBERS),
            help='Signal to send.' + help)
        pid_context.add_arguments(parser)

    def run(args):
        return send_signal(args.signal, args.pid_filename)

    return add_arguments, run

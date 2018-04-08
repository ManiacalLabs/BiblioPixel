import contextlib, signal

SIGNAL_NUMBERS = {k: v for k, v in signal.__dict__.items()
                  if k.startswith('SIG') and '_' not in k}

SIGNAL_NAMES = {v: k for k, v in SIGNAL_NUMBERS.items()}


@contextlib.contextmanager
def context(**handlers):
    signals = {}

    def handler(signum, frame):
        signame = SIGNAL_NAMES[signum]
        signals[signame] = True
        handler = handlers[signame]
        handler()

    for signame in handlers:
        if signame in SIGNAL_NUMBERS:  # Windows doesn't have all signals
            signal.signal(SIGNAL_NUMBERS[signame], handler)

    try:
        yield signals

    finally:
        for signame in handlers:
            if signame in SIGNAL_NUMBERS:  # Windows doesn't have all signals
                signal.signal(SIGNAL_NUMBERS[signame], signal.SIG_DFL)

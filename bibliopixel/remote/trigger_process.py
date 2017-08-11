import loady


def run_trigger(typename, q, events, kwargs):
    trigger_class = loady.code.load(typename)
    trigger = trigger_class(q, events, **kwargs)
    try:
        trigger.start()
    except KeyboardInterrupt:
        pass

from ... project import load


def run_trigger(typename, q, events, kwargs):
    trigger_class = load.code(typename)
    trigger = trigger_class(q, events, **kwargs)
    try:
        trigger.start()
    except KeyboardInterrupt:
        pass

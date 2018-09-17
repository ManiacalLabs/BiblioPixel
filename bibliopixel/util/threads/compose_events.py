import functools, threading


def compose_events(events, condition=all):
    """
    Compose a sequence of events into one event.

    Arguments:
        events:    a sequence of objects looking like threading.Event
        condition: a function taking a sequence of bools and returning a bool.
    """
    events = list(events)
    master_event = threading.Event()

    def changed():
        if condition(e.is_set() for e in events):
            master_event.set()
        else:
            master_event.clear()

    def add_changed(f):
        @functools.wraps(f)
        def wrapped():
            f()
            changed()

        return wrapped

    for e in events:
        e.set = add_changed(e.set)
        e.clear = add_changed(e.clear)

    changed()
    return master_event

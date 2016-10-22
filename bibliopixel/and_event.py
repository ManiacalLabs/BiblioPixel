import threading

# See https://stackoverflow.com/questions/12317940/

def and_set(self):
    self._set()
    self.changed()


def and_clear(self):
    self._clear()
    self.changed()


def andify(e, changed_callback):
    e._set = e.set
    e._clear = e.clear
    e.changed = changed_callback
    e.set = lambda: and_set(e)
    e.clear = lambda: and_clear(e)


def AndEvent(events):
    and_event = threading.Event()

    def changed():
        bools = [e.is_set() for e in events]
        if all(bools):
            and_event.set()
        else:
            and_event.clear()
    for e in events:
        andify(e, changed)
    changed()
    return and_event

# New implementation.

def compose_events(events, condition=all):
    """Compose a sequence of events into one event.
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
        def result():
            f()
            changed()
        return result

    for e in events:
        e.set = add_changed(e.set)
        e.clear = add_changed(e.clear)

    changed()
    return master_event

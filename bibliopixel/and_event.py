import threading


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

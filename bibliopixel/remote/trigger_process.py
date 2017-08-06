from .. util import importer


def run_trigger(typename, q, events, kwargs):
    trigger_class = importer.import_symbol(typename)
    trigger = trigger_class(q, events, **kwargs)
    try:
        trigger.start()
    except KeyboardInterrupt:
        pass

from .. util import importer


def run_trigger(typename, q, configs):
    trigger_class = importer.import_symbol(typename)
    trigger = trigger_class(q, configs)
    try:
        trigger.start()
    except KeyboardInterrupt:
        pass

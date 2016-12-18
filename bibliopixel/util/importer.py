import importlib


def import_path(name):
    """Import a module or symbol within a module at a given path."""
    try:
        return importlib.import_module(name)

    except ImportError as e:
        parts = name.split('.')
        if len(parts) > 1:
            symbol = parts.pop()
            namespace = import_path('.'.join(parts))
            try:
                return getattr(namespace, symbol)
            except AttributeError:
                pass
        raise e

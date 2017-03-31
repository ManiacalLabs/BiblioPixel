import importlib


def import_symbol(typename, package=None):
    """Import a module or typename within a module from its name."""
    try:
        return importlib.import_module(typename, package=package)

    except ImportError as e:
        parts = typename.split('.')
        if len(parts) > 1:
            typename = parts.pop()

            # Call import_module recursively.
            namespace = import_symbol('.'.join(parts), package=package)

            try:
                return getattr(namespace, typename)
            except AttributeError:
                pass
        raise

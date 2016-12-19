import importlib


def import_symbol(typename):
    """Import a module or typename within a module from its name."""
    try:
        return importlib.import_module(typename)

    except ImportError as e:
        parts = typename.split('.')
        if len(parts) > 1:
            typename = parts.pop()

            # Call import_module recursively.
            namespace = import_symbol('.'.join(parts))

            try:
                return getattr(namespace, typename)
            except AttributeError:
                pass
        raise e

    except:
        raise


def make_object(*args, typename, **kwds):
    """Make an object from a symbol."""
    return import_symbol(typename)(*args, **kwds)

from .. project import construct
from .. util import flatten
from . action import ActionList
from . receiver import Receiver


class Routing(Receiver):
    """
    A dict that routes a message to an ActionList.
    """

    def __init__(self, routing, default, python_path):
        """
        :param dict routing: `routing` is a dict that maps addresses
           to lists of actions.

           The values in the input dictionary `routing` are recursively visited
           to build the routing table:

           * values that are strings or lists are used to construct ActionLists
           * dictionaries that contain "typename" or "datatype" keys are
             used to construct a class of that type.
           * otherwise, dictionaries are visited recursively
           * all other types are forbidden
        """
        def make(x):
            if isinstance(x, (list, str)):
                return ActionList(x)

            assert isinstance(x, dict)
            if 'datatype' in x or 'typename' in x:
                x = dict(default, **x)
                return construct.construct_type(x, python_path)

            return {k: make(v) for k, v in x.items()}

        routing = flatten.unflatten(routing)
        self.routing = make(routing)

    def set_root(self, root):
        """Set the base project for routing."""
        def visit(x):
            # Try to set_root, then recurse through any values()
            set_root = getattr(x, 'set_root', None)
            if set_root:
                set_root(root)
            values = getattr(x, 'values', lambda: ())
            for v in values():
                visit(v)

        visit(self.routing)

    def receive(self, msg):
        """
        Returns a (receiver, msg) pair, where receiver is `None` if no route for
        the message was found, or otherwise an object with a `receive` method
        that can accept that `msg`.
        """
        x = self.routing
        while not isinstance(x, ActionList):
            if not x or not msg:
                return None, msg

            if not isinstance(x, dict):
                raise ValueError('Unexpected type %s' % type(x))

            _, value = msg.popitem(last=False)
            x = x.get(str(value))

        return x, msg

    def __bool__(self):
        return bool(self.routing)

    def __str__(self):
        return str(self.routing)

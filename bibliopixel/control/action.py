from . ops import Ops
from . editor import Editor
from . receiver import Receiver


class Action(Receiver):
    """
    An Action takes an incoming message, applies Ops to it, and then
    uses it to set a value on a Editor.
    """

    def __init__(self, address, ops=()):
        self.address = Editor(address)
        self.ops = Ops(*ops)

    def set_root(self, root):
        self.address.set_root(root)

    def receive(self, values):
        if self.ops:
            if len(values) == 1:
                values = [self.ops(values[0])]
            else:
                # TODO: They specified ops, but we can't use it.
                # Should we warn here?  Can we use the ops somehow?
                pass
        return self.address.receive(values)

    def __bool__(self):
        return bool(self.address or self.ops)

    def __str__(self):
        if self.ops:
            return '%s->%s' % self.address, self.ops
        return str(self.address)

    @classmethod
    def make(cls, action):
        if isinstance(action, str):
            return cls(action)
        if isinstance(action, dict):
            return cls(**action)
        return cls(*action)


class ActionList(Receiver):
    """A list of Actions."""

    def __init__(self, actions=None):
        if isinstance(actions, (str, dict)):
            actions = [actions]
        self.actions = tuple(Action.make(a) for a in actions or ())

    def set_root(self, root):
        for a in self.actions:
            a.set_root(root)

    def receive(self, msg):
        values = tuple(msg.values())
        for a in self.actions:
            a.receive(values)

    def __bool__(self):
        return bool(self.actions)

    def __str__(self):
        return ' + '.join(str(a) for a in self.actions)

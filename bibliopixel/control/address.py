"""
An address identifies how to get or set a piece of data within a Python object
using attributes and indexing.

An address description is a string looking like:

::

    .foo.bar[32][5][baz].bang()

which would mean

"given an object target, the value ``target.foo.bar[32][5]['baz'].bang()``".

Addresses are divided into "segments".

A segment contained in brackets ``[]`` is an index (for a list) or a key (for
a dictionary) - otherwise, it's an attribute.

In the example above, the segments are ``foo``, ``bar``, ``[32]``, ``[5]``,
``[baz]`` and ``bang``; ``foo`` and ``bar`` are attributes.
``baz`` is a string index, and ``32`` and ``5`` are numeric indexes.

You can use an Address to either get or set values in a target object.

Any key that's entirely numeric is taken to be an integer index.  This is
convenient but prevents the creation of dictionaries like ``{1: 'x', '1': 'y'}``
which probably didn't want to do that anyway.
"""

from .. util import log


class Address:
    class Segment:
        def __init__(self, name):
            self.name = name

        def set(self, target, *value):
            self._set(target, (value[0] if len(value) == 1 else value))

    class Attribute(Segment):
        def get(self, target):
            return getattr(target, self.name)

        def _set(self, target, value):
            setattr(target, self.name, value)

        def __str__(self):
            return '.%s' % self.name

    class Index(Segment):
        def get(self, target):
            return target[self.name]

        def _set(self, target, value):
            target[self.name] = value

        def __str__(self):
            return '[%s]' % self.name

    class Call(Segment):
        def __init__(self):
            pass

        def get(self, target):
            return target()

        def set(self, target, *value):
            target(*value)

        def __str__(self):
            return '()'

    def __init__(self, name=None):
        if not name:
            self.segments = self.assignment = ()
            return

        self.name, *assignment = name.split('=', 1)
        self.name = self.name.strip()

        try:
            self.segments = list(_generate(self.name))
        except:
            raise ValueError('%s is not a legal address' % name)

        if not self.segments:
            raise ValueError('Empty Addresses are not allowed')

        if assignment:
            if not self.segments:
                raise ValueError('Cannot assign to an empty address')
            if isinstance(self.segments[-1], Address.Call):
                raise ValueError('Cannot assign to a call operation')
            assignment = [s.strip() for s in assignment[0].split(',')]
            assignment = [int(s) if s.isnumeric() else s for s in assignment]
            self.assignment = tuple(assignment)
        else:
            self.assignment = ()

    def __bool__(self):
        return bool(self.segments)

    def __str__(self):
        return self.name

    @staticmethod
    def _get(target, address):
        for a in address:
            target = a.get(target)
        return target

    def get(self, target):
        return self._get(target, self.segments)

    def set(self, target, *values):
        *first, last = self.segments
        parent = self._get(target, first)
        last.set(parent, *(self.assignment + values))


def _generate(s):
    def extract_calls(p):
        # Extract () pairs from start and finish of a string
        before, after = [], []
        while p.startswith('()'):
            before.append(Address.Call())
            p = p[2:]

        while p.endswith('()'):
            after.append(Address.Call())
            p = p[:-2]

        return before, p, after

    # Split on dots, then use [ and ] to split out indices
    s = s.strip()
    if s.startswith('.'):
        s = s[1:]
    if s.endswith('.'):
        raise ValueError

    for i, part in enumerate(s.split('.')):
        if not part:
            raise ValueError

        head, *rest = part.split('[')

        # If we had e.g. 'xxx()()[yyy]()[zzz]()()'
        # Now we have first='xxx()' and rest = 'yyy]()', 'zzz]()()'
        # They might have written: ()xxx by mistake
        before, head, after = extract_calls(head)

        if before:
            # A call () is only allowed to start the first segment -
            # for example, an address like a.() is forbidden.
            if i or head:
                raise ValueError
            yield from before

        elif head:
            yield Address.Attribute(head)
            yield from after

        elif i:
            # An index [] is only allowed to start the first segment -
            # for example, an address like a.[2] is forbidden.
            raise ValueError

        for r in rest:
            before, r, after = extract_calls(r)
            if before:
                # A segment cannot contain a () - they must all be at top level.
                raise ValueError

            # A segment must have exactly one ']', exactly at the end.
            index, between = r.split(']', 1)
            if between:
                raise ValueError

            index = int(index) if index.isdigit() else index
            yield Address.Index(index)
            yield from after

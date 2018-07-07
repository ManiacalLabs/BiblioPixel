"""
An address identifies how to get or set a piece of data within a Python object,
called the "root", using attributes and indexing.

An address description is a string looking like:

::

    .foo.bar[32][5][baz].bang()

which would mean

"given an object "root", the value ``root.foo.bar[32][5]['baz'].bang()``".

Addresses are divided into "segments".

A segment contained in brackets ``[]`` is an index (for a list) or a key (for
a dictionary) - otherwise, it's an attribute.

In the example above, the segments are ``foo``, ``bar``, ``[32]``, ``[5]``,
``[baz]`` and ``bang``; ``foo`` and ``bar`` are attributes.
``baz`` is a string index, and ``32`` and ``5`` are numeric indexes.

You can use an Address to either get or set values in the root object.

Any key that's entirely numeric is taken to be an integer index.  This is
convenient but prevents the creation of dictionaries like ``{1: 'x', '1': 'y'}``
which you probably didn't want to do anyway.
"""

from .. util import data_file, log


def number(s):
    try:
        return data_file.loads(s)
    except:
        return s


class Address:
    class Segment:
        def __init__(self, name):
            self.name = name

        def set(self, root, *value):
            self._set(root, (value[0] if len(value) == 1 else value))

    class Attribute(Segment):
        def get(self, root):
            return getattr(root, self.name)

        def _set(self, root, value):
            setattr(root, self.name, value)

        def __str__(self):
            return '.%s' % self.name

    class Index(Segment):
        def get(self, root):
            return root[self.name]

        def _set(self, root, value):
            root[self.name] = value

        def __str__(self):
            return '[%s]' % self.name

    class Call(Segment):
        def __init__(self):
            pass

        def get(self, root):
            return root()

        def set(self, root, *value):
            root(*value)

        def __str__(self):
            return '()'

    def __init__(self, name=None):
        if not name:
            self.segments = self.assignment = ()
            return

        self.name, *assignment = name.split('=', 1)
        assignment = assignment and assignment[0].strip()

        self.name = self.name.strip()

        try:
            self.segments = list(_generate(self.name))
        except:
            raise ValueError('%s is not a legal address' % name)

        if not self.segments:
            raise ValueError('Empty Addresses are not allowed')

        if not assignment:
            self.assignment = ()
            return

        if isinstance(self.segments[-1], Address.Call):
            raise ValueError('Cannot assign to a call operation')

        self.assignment = tuple(number(s) for s in assignment.split(','))

    def __bool__(self):
        return bool(self.segments)

    def __str__(self):
        return self.name

    @staticmethod
    def _get(root, address):
        for a in address:
            root = a.get(root)
        return root

    def get(self, root):
        return self._get(root, self.segments)

    def set(self, root, *values):
        *first, last = self.segments
        parent = self._get(root, first)
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

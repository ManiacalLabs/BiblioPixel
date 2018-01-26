"""
An address identifies how to get or set a piece of data within a Python object
using attributes and indexing.

An address description is a string looking like:

    .foo.bar[32][5][baz].bang

which would mean

"given an object x, the value x.foo.bar[32][5]['baz'].bang".

Addresses are divided into "segments".  Segments in brackets are indexes or keys;
otherwise they are attributes.  In the example above, the segments are
foo, bar, [32], [5], [baz] and bang; foo and bar are attributes.
baz is a string index, and 32 and 5 are numeric indexes.

You can use addresses to either get or set values in an object. Getting or
setting throw a ValueError if the address can't be get or set, so calling code
that needs to be robust even in the face of bad user data will have to catch and
report or handle the error.

Numerical indexes are automatically distinguished from string indexes.  This is
convenient for the user but prevents them from having dictionaries like
{1: 'number one', '1': 'string one'} - they probably didn't want to do that
anyway.
"""


class Address:
    class Segment:
        def __init__(self, name):
            self.name = name

        def set(self, x, *value):
            return self._set(x, (value[0] if len(value) == 1 else value))

    class Attribute(Segment):
        def get(self, x):
            return getattr(x, self.name)

        def _set(self, x, value):
            return setattr(x, self.name, value)

    class Index(Segment):
        def get(self, x):
            return x[self.name]

        def _set(self, x, value):
            x[self.name] = value

    def __init__(self, s):
        def generate(s):
            # Split on dots, then use [ and ] to split out indices
            s = s.strip()
            while s.startswith('.'):
                s = s[1:]
            while s.endswith('.'):
                s = s[:-1]
            for i, part in enumerate(s.split('.')):
                head, *rest = part.split('[')

                # Suppose our address was 'xxx[yyy][zzz]'
                # Now we have first='xxx' and rest = 'yyy]', 'zzz]'
                if head:
                    yield Address.Attribute(head)
                elif i:
                    # An index [] is only allowed to start the *first* segment -
                    # for example, an address like a.[2] is forbidden.
                    raise ValueError

                for r in rest:
                    # A segment must have exactly one ']', exactly at the end.
                    index, between = r.split(']')
                    if between:
                        raise ValueError

                    try:
                        index = int(index)
                    except ValueError:
                        pass

                    yield Address.Index(index)

        try:
            self.address = list(generate(s))
        except:
            raise ValueError('%s is not a legal address' % s)

        if not self.address:
            raise ValueError('Empty Addresses are not allowed')

    @staticmethod
    def _get(x, address):
        for a in address:
            x = a.get(x)
        return x

    def get(self, x):
        return self._get(x, self.address)

    def set(self, x, *value):
        *first, last = self.address
        parent = self._get(x, first)
        last.set(parent, *value)

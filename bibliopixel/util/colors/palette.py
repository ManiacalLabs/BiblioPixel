import functools
from . classic import Black


class Palette(list):
    """
    Palette is a list of one or more colors used to render Animations.

    The method ``Palette.get()`` takes a position in the pallete and returns
    a color.
    """

    def __init__(self, colors=(), continuous=False, serpentine=False, scale=1,
                 offset=0):
        """
        Arguments:
            colors: an iterable of colors

            continuous: if True, interpolate linearly between colors; if False,
              use the nearest color from the original list

            serpentine: if True, pallete colors are used in reverse order every
              other iteration, giving a back-and-forth effect.  If False,
              palette colors always restart on each iteration

            scale: scales the incoming index ``i``.  As ``i`` moves from 0
              to ``len(colors) - 1``, the whole palette repeats itself
              ``self.scale`` times

            offset: offset to the incoming index  ``i``, applied after scaling
        """
        super().__init__(colors)
        if not self:
            self.append(Black)

        self.continuous = continuous
        self.serpentine = serpentine
        self.scale = scale
        self.offset = offset

    def get(self, position):
        """
        Return a color interpolated from the Palette. ``i`` may be any integer
        or floating point number.

        In the case where continuous=False, serpentine=False, scale=1 and
        offset=0, this is exactly the same as plain old [] indexing, but with a
        wrap-around.  The parameters affect this result as documented in the
        constructor.
        """
        pos = self._position(position * self.scale + self.offset)
        index = int(pos)
        fade = pos - index
        if not fade:
            return self[index]

        r1, g1, b1 = self[index]
        r2, g2, b2 = self[(index + 1) % len(self)]
        dr, dg, db = r2 - r1, g2 - g1, b2 - b1

        return r1 + fade * dr, g1 + fade * dg, b1 + fade * db

    def _position(self, i):
        n = len(self)
        if n == 1:
            return 0

        if not self.continuous:
            if not self.serpentine:
                return int(i % n)

            # We want a color sequence of length 2n-2
            # e.g. for n=5: a b c d | e d c b | a b c d ...
            m = (2 * n) - 2
            index = i % m
            return int(index if index < n else m - index)

        if not self.serpentine:
            index = i % n
        else:
            index = i % (2 * n)
            if index > n:
                index = (2 * n) - index

        # This is a number in [0, n): scale it to be in [0, n-1)
        return index * (n - 1) / n

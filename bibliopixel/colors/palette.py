import functools
from . classic import Black


class Palette(list):
    """
    Palette is a list of one or more colors used to render Animations.

    The method ``Palette.get()`` takes a position in the pallete and returns
    a color.
    """

    def __init__(self, colors=(), continuous=False, serpentine=False, scale=1,
                 offset=0, autoscale=False, length=None):
        """
        Arguments:
            colors: an iterable of colors

            continuous: if True, interpolate linearly between colors; if False,
              use the nearest color from the original list

            serpentine: if True, palette colors are used in reverse order every
              other iteration, giving a back-and-forth effect.  If False,
              palette colors always restart on each iteration

            scale: Scales the incoming index ``i``.  As ``i`` moves from 0
              to ``len(colors) - 1``, the whole palette repeats itself
              ``self.scale`` times

            offset: offset to the incoming index ``i``, applied after scaling

            autoscale: If True, automatically rescale the Palette size to
              match the length of the output.  ``autoscale`` happens before
              ``scale``, so the two work well together to give banding or
              striping effects across your display

           ``length``:
             The length of the output color_list.  If None, use the length of
             the palette itself.  If autoscale=True, ``length`` is used to scale
             the palette to match the output.
        """
        super().__init__(colors)
        if not self:
            self.append(Black)

        self.continuous = continuous
        self.serpentine = serpentine
        self.scale = scale
        self.offset = offset
        self.autoscale = autoscale
        self.length = length

    def __call__(self, position=0):
        return self.get(position)

    def get(self, position=0):
        """
        Return a color interpolated from the Palette.

        In the case where continuous=False, serpentine=False, scale=1,
        autoscale=False, and offset=0, this is exactly the same as plain old []
        indexing, but with a wrap-around.

        The constructor parameters affect this result as documented in the
        constructor.

        Arguments:
           ``position``:
             May be any integer or floating point number
        """
        n = len(self)
        if n == 1:
            return self[0]

        pos = position

        if self.length and self.autoscale:
            pos *= len(self)
            pos /= self.length

        pos *= self.scale
        pos += self.offset

        if not self.continuous:
            if not self.serpentine:
                return self[int(pos % n)]

            # We want a color sequence of length 2n-2
            # e.g. for n=5: a b c d | e d c b | a b c d ...
            m = (2 * n) - 2
            pos %= m
            if pos < n:
                return self[int(pos)]
            else:
                return self[int(m - pos)]

        if self.serpentine:
            pos %= (2 * n)
            if pos > n:
                pos = (2 * n) - pos
        else:
            pos %= n

        # p is a number in [0, n): scale it to be in [0, n-1)
        pos *= n - 1
        pos /= n

        index = int(pos)
        fade = pos - index
        if not fade:
            return self[index]

        r1, g1, b1 = self[index]
        r2, g2, b2 = self[(index + 1) % len(self)]
        dr, dg, db = r2 - r1, g2 - g1, b2 - b1

        return r1 + fade * dr, g1 + fade * dg, b1 + fade * db

    def __eq__(self, other):
        return (isinstance(other, Palette) and
                super().__eq__(other) and
                vars(self) == vars(other))

    def __ne__(self, other):
        return not (self == other)

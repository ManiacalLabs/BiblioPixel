from . classic import Black


class Palette(list):
    """
    Palette is a list of one or more colors used to render Animations.

    The method ``Palette.interpolate()`` takes a ``phase`` and returns a color
    from the palette.

    ``phase`` can be any numeric value, but varying ``phase`` between from
    0 to 1 typically means "one repetition".
    """

    def __init__(self, colors=(), continuous=True, serpentine=False, scale=1):
        """
        Arguments:
            colors: an iterable of colors

            continuous: if True, interpolate linearly between colors; if False,
              use the nearest color from the original list.

            serpentine: if True, pallete colors are used in reverse order every
              other iteration, giving a back-and-forth effect.  If False,
              palette colors always restart on each iteration

            scale: scales the incoming ``phase``.  As ``phase`` moves from 0
              to 1, the whole palette repeats itself ``self.scale`` times
        """
        super().__init__(colors)
        if not self:
            self.append(Black)

        self.continuous = continuous
        self.serpentine = serpentine
        self.scale = scale

    def interpolate(self, phase):
        """
        Returns a color interpolated from the palette.

        Arguments:
            phase:  any numeric value (where the range [0, 1] is canonically
                "one repetition")
        """
        n = len(self)
        if n == 1:
            return self[0]

        cycle, phase = divmod(phase * self.scale, 1)
        odd_numbered_cycle = self.serpentine and (int(cycle) & 1)

        if not self.continuous:
            if self.serpentine:
                # We want a color sequence like a b c d | e d c b | a
                color_index = int((n - 1) * phase)
                if odd_numbered_cycle:
                    color_index = (n - 1) - color_index
            else:
                # We want a sequence like a b c d e | a b c d e
                color_index = int(phase * n)

            return self[color_index]

        if odd_numbered_cycle:
            if not phase:
                return self[-1]
            phase = 1 - phase

        position = phase * (n - 1)
        index, fade = divmod(position, 1)
        index = int(index)
        r1, g1, b1 = self[index]
        r2, g2, b2 = self[index + 1]
        dr, dg, db = r2 - r1, g2 - g1, b2 - b1

        return r1 + fade * dr, g1 + fade * dg, b1 + fade * db

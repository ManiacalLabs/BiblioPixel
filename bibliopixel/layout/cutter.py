"""
Cut matrices by row or column and apply operations to them.
"""


class Cutter:
    """
    Base class that pre-calculates cuts and can use them to
    apply a function to the layout.

    Each "cut" is a row or column, depending on the value of by_row.

    The entries are iterated forward or backwards, depending on the
    value of forward.
    """

    def __init__(self, layout, by_row=True):
        self.layout = layout
        cuts = layout.height if by_row else layout.width
        cutter = self.cut_row if by_row else self.cut_column
        self.cuts = [cutter(i) for i in range(cuts)]

    def apply(self, function):
        """
        For each row or column in cuts, read a list of its colors,
        apply the function to that list of colors, then write it back
        to the layout.
        """
        for cut in self.cuts:
            value = self.read(cut)
            function(value)
            self.write(cut, value)


class Slicer(Cutter):
    """
    Implementation of Cutter that uses slices of the underlying colorlist.
    Does not work if the Matrix layout is serpentine or has any reflections
    or rotations.
    """

    def cut_row(self, i):
        return slice(self.layout.width * i, self.layout.width * (i + 1))

    def cut_column(self, i):
        return slice(i, None, self.layout.width)

    def read(self, cut):
        return self.layout.color_list[cut]

    def write(self, cut, value):
        self.layout.color_list[cut] = value


class Indexer(Cutter):
    """
    Slower implementation of Cutter that uses lists of indices and the
    Matrix interface.
    """

    def cut_row(self, i):
        return [(column, i) for column in range(self.layout.width)]

    def cut_column(self, i):
        return [(i, row) for row in range(self.layout.height)]

    def read(self, cut):
        return [self.layout.get(*i) for i in cut]

    def write(self, cut, value):
        for i, v in zip(cut, value):
            self.layout.set(*i, color=v)

from . animation import Animation
from .. util.colors import make


class Fill(Animation):
    """
    Fill the screen with a single color or a palette of colors
    """
    def __init__(self, *args, color=None, palette=None, **kwds):
        # Handle legacy "color" parameter
        if color:
            if palette:
                raise ValueError('At most one of color and pallete can be set')
            palette = make.colors(color)

        super().__init__(*args, preclear=False, palette=palette, **kwds)

    def step(self, amt=1):
        n = len(self.color_list)
        self.color_list[:] = (self.palette.get(i) for i in range(n))

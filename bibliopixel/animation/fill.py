from . animation import BaseAnimation
from .. util import colors


class Fill(BaseAnimation):
    """
    Fill the screen with a single color.
    """
    def __init__(self, *args, color='black', **kwds):
        super().__init__(*args, preclear=False, **kwds)

        is_numpy = hasattr(self.color_list, 'dtype')
        self._set_color = self._set_numpy if is_numpy else self._set_classic
        self._color = color

    def pre_run(self):
        self.color = self._color

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = colors.to_color(color)
        self._set_color()

    def _set_numpy(self):
        self.color_list[:None] = self._color

    def _set_classic(self):
        self.color_list[:] = [self._color] * len(self.color_list)

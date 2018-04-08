from . import wrapper
from .. util import color_list
from .. util.limit import Limit


class Limiter(wrapper.Wrapper):
    def __init__(self, *args, limit=None, **kwds):
        """
        :param dict limit: A construction dictionary for a Limit.
        """
        super().__init__(*args, **kwds)
        self.limit = Limit(**(limit or {}))
        self._math = color_list.Math(self.color_list)

    def pre_run(self):
        super().pre_run()
        self.animation.layout = self.layout.clone()

    def step(self, amt=1):
        super().step(amt)
        self._math.copy(self.color_list, self.animation.color_list)
        self.limit.limit_colors(self.color_list, self._math)

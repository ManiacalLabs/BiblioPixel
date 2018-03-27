import copy
from . import collection


class Parallel(collection.Collection):
    """
    A Parallel is a Collection where all the animations are running at the same
    time - as opposed to the base Collection where only one animation runs
    at any time.
    """
    def __init__(self, *args, overlay=False, **kwds):
        """
        If overlay is True, then preclear is set to False for everything
        other than the first animation.
        """
        super().__init__(*args, **kwds)

        # Give each animation a unique, mutable layout so they can
        # run independently.
        for i, a in enumerate(self.animations):
            a.layout = copy.deepcopy(a.layout)
            if overlay and i:
                a.preclear = False

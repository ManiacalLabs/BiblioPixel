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
        self.detach(overlay)

    def step(self, amt=1):
        for a in self.animations:
            a.step(amt)

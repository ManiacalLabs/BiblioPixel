from . import collection


class Parallel(collection.Collection):
    """
    A Parallel is a Collection where all the animations are running at the same
    time - as opposed to the base Collection where only one animation runs
    at any time.
    """

    def __init__(self, *args, overlay=False, detach=True, **kwds):
        """
        If overlay is True, then preclear is set to False for everything
        other than the first animation.
        """
        super().__init__(*args, **kwds)
        if detach:
            self.detach(overlay)

    def generate_frames(self):
        self._frames = [[a.generate_frames(), True] for a in self.animations]
        return super().generate_frames()

    def step(self, amt=1):
        for i, (frames, enabled) in enumerate(self._frames):
            if enabled:
                try:
                    next(frames)
                except StopIteration:
                    self._frames[i][1] = False

import functools, queue, traceback
from .. util import log


class EditQueue(queue.Queue):
    """
    ``Edits``s are thread-unsafe operations to be executed later at a
    thread-safe time.  In the animation loop, this happens in
    :py:method:`bibliopixel.animation.Animation.preframe_callback`.

    The typical `Edit` is a change to some parameter of an animation,
    but in general is represented by a call to a function with fixed parameters.
    """

    def put_edit(self, f, *args, **kwds):
        """
        Defer an edit to run on the EditQueue.

        :param callable f: The function to be called
        :param tuple args: Positional arguments to the function
        :param tuple kwds: Keyword arguments to the function
        :throws queue.Full: if the queue is full
        """
        self.put_nowait(functools.partial(f, *args, **kwds))

    def get_and_run_edits(self):
        """
        Get all the edits in the queue, then execute them.

        The algorithm gets all edits, and then executes all of them.  It does
        *not* pull off one edit, execute, repeat until the queue is empty, and
        that means that the queue might not be empty at the end of
        ``run_edits``, because new edits might have entered the queue
        while the previous edits are being executed.

        This has the advantage that if edits enter the queue faster than they
        can be processed, ``get_and_run_edits`` won't go into an infinite loop,
        but rather the queue will grow unboundedly, which that can be
        detected, and mitigated and reported on - or if Queue.maxsize is
        set, `bp` will report a fairly clear error and just dump the edits
        on the ground.
        """
        if self.empty():
            return

        edits = []
        while True:
            try:
                edits.append(self.get_nowait())
            except queue.Empty:
                break

        for e in edits:
            try:
                e()
            except:
                log.error('Error on edit %s', e)
                traceback.print_exc()

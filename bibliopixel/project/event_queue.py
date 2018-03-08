import functools, queue


class EventQueue(queue.Queue):
    """
    ``Event``s are thread-unsafe operations to be executed later at a
    thread-safe time.  In the animation loop, this happens in
    :py:method:`bibliopixel.animation.Animation.preframe_callback`.

    The typical `Event` is a change to some parameter of an animation,
    but in general is represented by a call to a function with fixed parameters.
    """

    def put_event(self, f, *args, **kwds):
        """
        Defer an event to run on the EventQueue.

        :param callable f: The function to be called
        :param tuple args: Positional arguments to the function
        :param tuple kwds: Keyword arguments to the function
        :throws queue.Full: if the queue is full
        """
        self.put_nowait(functools.partial(f, *args, **kwds))

    def get_and_run_events(self):
        """
        Get all the events in the queue, then execute them.

        The algorithm gets all events, and then executes all of them.  It does
        *not* pull off one event, execute, repeat until the queue is empty, and
        that means that the queue might not be empty at the end of
        ``run_events``, because new events might have entered the queue
        while the previous events are being executed.

        This has the advantage that if events enter the queue faster than they
        can be processed, ``get_and_run_events`` won't go into an infinite loop,
        but rather the queue will grow unboundedly, which that can be
        detected, and mitigated and reported on - or if Queue.maxsize is
        set, `bp` will report a fairly clear error and just dump the events
        on the ground.
        """
        if self.empty():
            return

        events = []
        while True:
            try:
                events.append(self.get_nowait())
            except queue.Empty:
                break

        for e in events:
            e()

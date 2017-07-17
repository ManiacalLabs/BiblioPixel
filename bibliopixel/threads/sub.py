"""
More or less uniformly run something as a new daemon thread or process.
"""

import multiprocessing, threading, queue


def _run_locally(input, output, function, args, **kwds):
    function(input, output, *args, **kwds)


def run(function, *args, use_subprocess=False, daemon=True, **kwds):
    """
    Create input, output queues, call `function` in a subprocess or a thread.

    `function` is called like this:
        function(input, output, *args, **kwds)

    Args:
        use_subprocess: if true, create a new multiprocess;  if false, create
            a new thread
        function: the function to call
        *args, **kwds: arguments to the function.
        daemon: is the thread or subprocess run as a daemon or not?

    Returns:
        a tuple with three elements: the subprocess or thread, an input
        queue, and an output queue.
    """
    if use_subprocess:
        Creator, Queue = multiprocessing.Process, multiprocessing.Queue
    else:
        Creator, Queue = threading.Thread, queue.Queue

    input, output = Queue(), Queue()
    args = input, output, function, args
    sub = Creator(target=_run_locally, args=args, kwargs=kwds, daemon=daemon)
    sub.start()

    return sub, input, output

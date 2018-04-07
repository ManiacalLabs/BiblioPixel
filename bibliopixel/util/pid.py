import contextlib, os
from . import log


@contextlib.contextmanager
def pid_context(pid_filename):
    if os.exists(pid_filename):
        contents = open(pid_filename).read(16)
        log.warning('PID filename already exists with contents %s...', contents)

    with open(pid_filename, 'w') as fp:
        fp.write(str(os.getpid()))
        fp.write('\n')

    yield
    try:
        os.remove(pid_filename)
    except Exception as e:
        log.error('Got an exception deleting the pid_filename %s: %s',
                  pid_filename, e)


def get_pid(pid_filename):
    """
    Return the integer PID for the current bp process, or raise an exception.
    """
    return int(open(pid_filename).read(16))

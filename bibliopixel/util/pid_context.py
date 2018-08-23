import contextlib, os, tempfile
from . import log

DEFAULT_PID_FILENAME = os.path.join(tempfile.gettempdir(), 'bp_pid_file.txt')


@contextlib.contextmanager
def pid_context(pid_filename):
    """
    For the duration of this context manager, put the PID for this process into
    `pid_filename`, and then remove the file at the end.
    """
    if os.path.exists(pid_filename):
        contents = open(pid_filename).read(16)
        log.warning('pid_filename %s already exists with contents %s...',
                    pid_filename, contents)

    with open(pid_filename, 'w') as fp:
        fp.write(str(os.getpid()))
        fp.write('\n')

    try:
        yield
    finally:
        try:
            os.remove(pid_filename)
        except Exception as e:
            log.error('Got an exception %s deleting the pid_filename %s',
                      e, pid_filename)


def get_pid(pid_filename):
    """
    Return the integer PID for the current bp process, or raise an exception if
    there is no such process or it hasn't registered a PID.
    """
    return int(open(pid_filename).read(16))

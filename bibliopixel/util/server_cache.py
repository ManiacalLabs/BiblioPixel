import errno
from . import log


ADDRESS_IN_USE_ERROR = """

Port {0} on your machine is already in use.
Perhaps BiblioPixel is already running on your machine?
"""

CACHED_SERVER_ERROR = """
Tried to open server of type {new_type} on port {port}, but there was already
a server of type {old_type} running there.
"""

CACHED_KWDS_WARNING = """
Cached server for port {server.port} had keywords {server.kwds},
but keywords {kwds} were requested.
"""


class CachedServer:
    def __init__(self, port, constructor, **kwds):
        self.server = self._make_server(port, constructor, **kwds)
        self.port = port
        self.constructor = constructor
        self.kwds = kwds

    def check_keywords(self, constructor, **kwds):
        if self.constructor != constructor:
            raise ValueError(CACHED_SERVER_ERROR.format(
                port=self.port,
                new_type=str(constructor),
                old_type=str(self.constructor)))

        if self.kwds != kwds:
            log.warning(CACHED_KWDS_WARNING.format(server=self, kwds=kwds))

    def close(self):
        pass

    def __getattr__(self, key):
        # Pass through all other attributes to the server.
        return getattr(self.server, key)

    @staticmethod
    def _make_server(port, constructor, **kwds):
        try:
            return constructor(port, **kwds)
        except OSError as e:
            if e.errno == errno.EADDRINUSE:
                e.strerror += ADDRESS_IN_USE_ERROR.format(port)
                e.args = (e.errno, e.strerror)
            raise


class ServerCache:
    ENABLE = True

    def __init__(self, **kwds):
        self.servers = {}
        self.kwds = kwds

    def get_server(self, port, **kwds):
        kwds = dict(self.kwds, **kwds)

        if not self.ENABLE:
            return CachedServer._make_server(port, **kwds)

        server = self.servers.get(port)
        if server:
            server.check_keywords(**kwds)
        else:
            server = CachedServer(port, **kwds)
            self.servers[port] = server

        return server

    def close(self, port):
        server = self.servers.pop(port)
        server.server.close()

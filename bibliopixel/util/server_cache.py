import errno
from .. import log


ADDRESS_IN_USE_ERROR = """

Cached server {0} on your machine is already in use.
Perhaps BiblioPixel is already running on your machine?
"""

CACHED_SERVER_ERROR = """
Tried to open server of type {new_type} on {port}, but there was already
a server of type {old_type} running there.
"""

CACHED_KWDS_WARNING = """
Cached server for {server.port} had keywords {server.kwds},
but keywords {kwds} were requested.
"""


class _CachedServer:
    def __init__(self, constructor, key, kwds):
        self.server = self._make_server(constructor, key, kwds)
        self.key = key
        self.constructor = constructor
        self.kwds = kwds

    def check_keywords(self, constructor, kwds):
        if self.constructor != constructor:
            raise ValueError(CACHED_SERVER_ERROR.format(
                key=self.key,
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
    def _make_server(constructor, key, kwds):
        try:
            return constructor(key, **kwds)
        except OSError as e:
            if e.errno == errno.EADDRINUSE:
                e.strerror += ADDRESS_IN_USE_ERROR.format(key)
                e.args = (e.errno, e.strerror)
            raise


class ServerCache:
    """
    A class that caches servers by key so you don't keep closing and re-opening
    the same server and interrupting your connection.

    The exact nature of the key depends on the sort of server.
    For example, for a server socket like SimPixel, it would be just a port
    number, whereas for a UDP connection like Art-Net, it would be a
    port, ip_address pair.
    """

    def __init__(self, constructor, **kwds):
        """
        :param constructor: a function which takes a key and some keywords,
            and returns a new server
        :param kwds: keywords to the ``constructor`` function
        """
        self.servers = {}
        self.constructor = constructor
        self.kwds = kwds

    def get_server(self, key):
        """
        Get a new or existing server for this key.

        :param int key: key for the server to use
        """
        server = self.servers.get(key)
        if server:
            # Make sure it's the right server.
            server.check_keywords(self.constructor, self.kwds)
        else:
            # Make a new server
            server = _CachedServer(self.constructor, key, self.kwds)
            self.servers[key] = server

        return server

    def close(self, key):
        server = self.servers.pop(key, None)
        if server:
            server.server.close()
            return True


class StaticCache:
    SERVER_CLASS = None
    SERVER_KWDS = {}
    CACHE = None

    @classmethod
    def cache(cls):
        if not cls.CACHE:
            cls.CACHE = ServerCache(cls.SERVER_CLASS, **cls.SERVER_KWDS)
        return cls.CACHE

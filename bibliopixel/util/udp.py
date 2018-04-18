"""
A server that queues and sends UDP requests for a specific port on a
separate thread.
"""

import queue, socket
from .. util.threads import runnable


class Sender(runnable.Runnable):
    def __init__(self, address):
        """
        :param str address: a pair (ip_address, port) to pass to socket.connect
        """
        super().__init__()
        self.address = address

    def send(self, msg):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.settimeout(self.timeout)
            sock.connect(self.address)
            sock.send(msg)
            # sock.sendto(msg, self.address)


class QueuedSender(runnable.QueueHandler):
    """
    The UPD protocol is stateless but not necessarily thread-safe.

    ``QueuedSender`` uses a queue to send all UDP messages to one address
    from a new thread.

    """

    def __init__(self, address, **kwds):
        """
        :param str address: a pair (ip_address, port) to pass to socket.connect
        """
        super().__init__(**kwds)
        self.sender = Sender(address)

    def send(self, msg):
        self.sender.send(msg)


def sender(address, use_queue=True, **kwds):
    """
    :param str address: a pair (ip_address, port) to pass to socket.connect
    :param bool use_queue: if True, run the connection in a different thread
        with a queue
    """
    return QueuedSender(address, **kwds) if use_queue else Sender(address)


class Receiver(runnable.Loop):
    """
    Receive UDP messages in a thread
    """

    def __init__(self, address, bufsize=0x1000, receive=None, **kwds):
        super().__init__(**kwds)
        self.address = address
        self.bufsize = bufsize
        self.receive = receive or self.receive

    def run(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(self.address)
        self.socket.settimeout(self.timeout)

        super().run()

    def loop(self):
        try:
            data, addr = self.socket.recvfrom(self.bufsize)
        except socket.timeout:
            return
        if data:
            self.receive(data)

    def receive(self, msg):
        pass


class QueuedReceiver(Receiver):
    """
    Receive UDP messages in a thread and put them on a queue.
    """

    def run(self):
        self.queue = queue.Queue()
        super().run()

    def receive(self, msg):
        self.queue.put(msg)

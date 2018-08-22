import threading, time, webbrowser
from ... util import log

WEBPAGE_OPENED = False


def opener(ip_address, port, delay=1):
    """
    Wait a little and then open a web browser page for the control panel.
    """
    global WEBPAGE_OPENED
    if WEBPAGE_OPENED:
        return
    WEBPAGE_OPENED = True
    raw_opener(ip_address, port, delay)


def raw_opener(ip_address, port, delay=1):
    """
    Wait a little and then open a web browser page for the control panel.
    """
    def target():
        time.sleep(delay)
        url = 'http://%s:%d' % (ip_address, port)
        webbrowser.open(url, new=0, autoraise=True)

    threading.Thread(target=target, daemon=True).start()

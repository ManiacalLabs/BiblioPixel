import webbrowser

DEFAULT_URL = 'http://simpixel.io'
SIMPIXEL_OPENED = False


def open_simpixel(url=None):
    global SIMPIXEL_OPENED
    if not SIMPIXEL_OPENED:
        url = url or DEFAULT_URL

        if not url.startswith('no'):
            webbrowser.open(url, new=0, autoraise=True)
            SIMPIXEL_OPENED = True

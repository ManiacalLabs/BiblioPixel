import webbrowser

DEFAULT_URL = 'http://simpixel.io'


def open_simpixel(url=None):
    url = url or DEFAULT_URL

    if not url.startswith('no'):
        webbrowser.open(url, new=0, autoraise=True)

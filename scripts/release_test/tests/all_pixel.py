import common

FEATURES = 'all_pixel',

LEDTYPES = 'WS2801', 'LPD8806', 'SK6812', 'WS2812', 'SK9822', 'APA102'
SYNONYMS = {'SK6812': 'WS2812B'}
MESSAGE = '%d: connect %s and press return. '


def run():
    for i, t in enumerate(LEDTYPES):
        input(MESSAGE % (i, t))
        common.run_project('all_pixel.yml', flag='-t=' + SYNONYMS.get(t, t))

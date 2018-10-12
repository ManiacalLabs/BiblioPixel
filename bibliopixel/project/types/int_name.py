from ... util import int_names

USAGE = """
An int_name is either an integer, a string representing an integer, or a
fanciful name that's either a day of week, a month, a planet, or a chemical
element.
"""


def make(c):
    try:
        return int_names.to_index(c)
    except:
        raise ValueError('Don\'t understand "%s"\n%s' % (c, USAGE))

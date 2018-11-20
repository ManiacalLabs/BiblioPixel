import itertools
from . import names


def closest_colors(color_name, metric=None):
    metric = metric or euclidean
    color = names.to_color(color_name)

    mn_list = [(metric(color, c), n) for n, c in names.COLOR_DICT.items()]
    mn_list.sort()
    min_metric = mn_list[0][0]
    result = []
    for met, name in mn_list:
        if met > min_metric:
            return sorted(result)
        result.append(name)


def euclidean(c1, c2):
    """Square of the euclidean distance"""
    diffs = ((i - j) for i, j in zip(c1, c2))
    return sum(x * x for x in diffs)


def taxicab(c1, c2):
    diffs = ((i - j) for i, j in zip(c1, c2))
    return sum(abs(x) for x in diffs)


def all_colors(start=0, stop=255, skip=1):
    return itertools.product(range(start, stop, skip), repeat=3)

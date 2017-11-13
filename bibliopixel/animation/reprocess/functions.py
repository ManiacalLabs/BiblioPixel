from ... util.colors.conversions import color_cmp


def sorter(x):
    if len(x) < 2:
        return

    prev = x[0]
    for i in range(1, len(x)):
        next = x[i]
        if color_cmp(prev, next) > 0:
            x[i - 1], x[i] = next, prev
            return
        prev = next


FUNCTIONS = {'sorter': sorter}

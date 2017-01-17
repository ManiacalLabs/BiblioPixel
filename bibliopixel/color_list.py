from . import timedata


def ColorList(n):
    if timedata.enabled():
        color_list = timedata.ColorList255()
        color_list.resize(n)
        return color_list
    return [(0, 0, 0)] * n


Renderer = timedata.Renderer
